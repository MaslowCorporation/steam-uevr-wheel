#define NOMINMAX
#define LOG_TAG "[VRSteering] "

#define _CRT_SECURE_NO_WARNINGS

// MAX_STEERING_ANGLE is the max steering angle used during the steering angle calculation.
// 180.0f is a good starting point foe the wheel steering angle.
// Play with this value, and find the sweet spot of reactiveness of the wheel.
// Some value between 90.0f and 180.0f is the best ! Play with it ;-)
#define MAX_STEERING_ANGLE 90.0f

// MAX_STEAM_VR_WHEEL_STEERING_ANGLE is the max steering angle of the visual VR wheel on screen.
// (the steam-vr-wheel overlay)
// This is the full range of motion of the wheel on both sides combined
// so if you set this to 360, the on screen wheel will steer 180 degrees to the left and 180 degrees to the right, AKA 360 degrees ;-)
#define MAX_STEAM_VR_WHEEL_STEERING_ANGLE 360

// the different steering directions available
#define STEERING_CLOCKWISE 0
#define STEERING_COUNTERCLOCKWISE 1
#define NO_STEERING 2

// the states of the VR wheel overlay
#define WHEEL_INVISIBLE 0
#define WHEEL_SETUP 1
#define WHEEL_VISIBLE 2

// the path of the config file of the steam-vr-wheel overlay
#define CONFIG_JSON_PATH "C:/Users/MaslowPatrick/AppData/Local/steam-vr-wheel/config.json"

// the path of the .bat file that starts the steam-vr-wheel overlay
#define STEAM_VR_WHEEL_PATH "C:/Users/MaslowPatrick/Downloads/steam-vr-wheel-2.5.4a/steam-vr-wheel-2.5.4a/steam-vr-wheel.bat"

// the duration of the wheel mode button timeout in milliseconds
#define WHEEL_MODE_BUTTON_TIMEOUT_MSEC 1000

// PI is delicious ;-)
#define PI 3.14159265358979323846f

#include <zmq.hpp>
#include <windows.h>
#include <cmath>
#include "Dependencies/uevr/Plugin.hpp"
#include "Dependencies/nlohmann/json.hpp"
#include <chrono> // For timing
#include <fstream>
#include <iostream>
#include <memory>
#include <vector>
#include <thread>
#include <shlobj.h>		// For SHGetKnownFolderPath
#include <combaseapi.h> // For CoTaskMemFre
#include <filesystem>

using namespace uevr;
using namespace std::chrono;

struct Vector2f
{
	float x, y;
};

class VRHands : public uevr::Plugin
{
public:
	VRHands() : precise_steering_angle_degrees(0.0f),
				wheel_grabbed(false),
				wheel_status(WHEEL_INVISIBLE),
				steam_vr_wheel_started(false),
				wheel_mode_button_timeout(false) {}

	// destructor function that runs when shizzle gets destroyed
	virtual ~VRHands()
	{
		// stop the socket server thread
		stop_socket_server();

		// Stop the .exe file
		stop_exe(wheel_process);

		log_debug_message("Bye amigo ;-)");
	}

	void on_dllmain() override {}

	// callback that does initialization work before starting the plugin
	void on_initialize() override
	{
		log_debug_message("VR Steering Wheel plugin has started ;-)");

		// reset the config.json object of the steam-vr-wheel
		// this object is located at CONFIG_JSON_PATH
		reset_steam_vr_wheel_settings();

		// start the steam-uevr-wheel .exe file located in the Documents folder.
		start_steam_uevr_wheel_exe();
	}

	// start the steam-uevr-wheel .exe file located in the Documents folder.
	void start_steam_uevr_wheel_exe()
	{
		// path of the steam-uevr-wheel executable
		char *documents_folder_char = get_documents_folder();
		std::filesystem::path documents_folder(documents_folder_char);
		std::filesystem::path steam_uevr_exe_path = "steam-uevr-wheel\\open-vr-wheel.exe";
		std::filesystem::path full_steam_uevr_exe_path = documents_folder / steam_uevr_exe_path;

		LPWSTR full_steam_uevr_exe_path_lp = pathToLPWSTR(full_steam_uevr_exe_path);

		// start the shizzle
		wheel_process = start_exe(full_steam_uevr_exe_path_lp);
	}

	// start an .exe file from it's file path
	PROCESS_INFORMATION start_exe(const std::filesystem::path &exePath)
	{
		LPWSTR path = pathToLPWSTR(exePath);

		STARTUPINFO startupInfo = {sizeof(STARTUPINFO)};
		PROCESS_INFORMATION processInfo = {};
		BOOL success = CreateProcess(
			path, // lpApplicationName
			NULL, // lpCommandLine
			NULL, // lpProcessAttributes
			NULL, // lpThreadAttributes
			TRUE, // bInheritHandles
			0,	  // dwCreationFlags
			NULL, // lpEnvironment
			NULL, // lpCurrentDirectory
			&startupInfo,
			&processInfo);

		return processInfo;
	}

	// stop an .exe file from it's PROCESS_INFORMATION object
	void stop_exe(PROCESS_INFORMATION &processInfo)
	{
		// Terminate the process
		TerminateProcess(processInfo.hProcess, 0);

		// Close handles
		CloseHandle(processInfo.hThread);
		CloseHandle(processInfo.hProcess);
	}

	// Function to convert std::filesystem::path to LPWSTR
	LPWSTR pathToLPWSTR(const std::filesystem::path &path)
	{
		// Extract the wide string from std::filesystem::path
		std::wstring wstr = path.wstring();

		// Allocate new wide string
		LPWSTR lpwstr = new wchar_t[wstr.size() + 1];
		wcscpy(lpwstr, wstr.c_str()); // Copy the wide string

		return lpwstr;
	}

	// get the path of the Documents folder on Windows
	char *get_documents_folder()
	{
		PWSTR path = nullptr;
		HRESULT result = SHGetKnownFolderPath(FOLDERID_Documents, 0, nullptr, &path);
		char buffer[MAX_PATH];

		if (SUCCEEDED(result))
		{
			// Convert from wide string to narrow string

			wcstombs(buffer, path, MAX_PATH);
			log_debug_message("Documents Path: %s", buffer);
		}
		else
		{
			log_debug_message("Error: Unable to get the Documents path.");
		}

		// Free memory allocated by SHGetKnownFolderPath
		if (path)
		{
			CoTaskMemFree(path);
		}

		return buffer;
	}

	// start the socket server that grabs the current steam-vr-wheel angle from the python (steam-vr-wheel) side of this plugin,
	// thanks to ZeroMQ socket mechanism
	void launch_socket_server(std::stop_token s)
	{
		log_debug_message("Let's start the socket server");

		// initialize the zmq context with a single IO thread
		zmq::context_t context{1};

		// construct a PULL socket and bind to interface
		zmq::socket_t socket{context, zmq::socket_type::pull};

		socket.bind("tcp://*:65435");

		log_debug_message("socket server started !");

		while (!s.stop_requested())
		{
			zmq::message_t request;

			// receive a request from client
			auto request_output = socket.recv(request, zmq::recv_flags::none);

			precise_steering_angle_degrees = std::stof(request.to_string());

			// log_debug_message("deg: %f", precise_steering_angle_degrees);
		}

		// stop the socket server thread
		// stop_socket_server();
	}

	// Allows you to print debug messages that can be viewed externally through DbgView, in real time.
	void log_debug_message(const char *format, ...)
	{
		char buffer[256];
		va_list args;
		va_start(args, format);

		// Construct the message with the log tag
		_snprintf_s(buffer, sizeof(buffer), LOG_TAG);										 // Add the tag to the buffer
		vsnprintf(buffer + strlen(LOG_TAG), sizeof(buffer) - strlen(LOG_TAG), format, args); // Append the message

		va_end(args);
		OutputDebugStringA(buffer);
	}

	// callback that resets the steam-vr-wheel config JSON object right before starting the plugin
	void reset_steam_vr_wheel_settings()
	{
		// contains the JSON object of the steam-vr-wheel options
		nlohmann::json steam_vr_wheel_options = getJSONObject(CONFIG_JSON_PATH);

		// - set wheel_status to WHEEL_INVISIBLE
		wheel_status = WHEEL_INVISIBLE;

		// - set the wheel_show_wheel property of the JSON object in CONFIG_JSON_PATH to false,
		steam_vr_wheel_options["wheel_show_wheel"] = false;

		// - set the wheel_show_hands property of the JSON object in CONFIG_JSON_PATH to false,
		steam_vr_wheel_options["wheel_show_hands"] = false;

		// save the steam-vr-wheel config edits
		setJSONObject(CONFIG_JSON_PATH, steam_vr_wheel_options);
	}

	// callback that gets executed right before the current tick
	void on_pre_engine_tick(API::UGameEngine *engine, float delta) override
	{
		UEVR_Vector3f left_position;
		UEVR_Quaternionf left_rotation;
		UEVR_Vector3f right_position;
		UEVR_Quaternionf right_rotation;

		const auto everything_is_ready = get_controllers_positions_and_rotations(
			&left_position,
			&right_position,
			&left_rotation,
			&right_rotation);

		// handle the wheel mode button press (the right VR controller grip button)
		handle_wheel_mode_button_timeout(everything_is_ready);

		// handle the wheel grab button (the left VR controller grip button)
		handle_wheel_grab_button(
			everything_is_ready);
	}

	// gives you a string representation of the current wheel status state
	// (the wheel status is the state of the wheel, one of WHEEL_INVISIBLE = 0, WHEEL_SETUP = 1, and WHEEL_VISIBLE = 2)
	const char *get_wheel_status_str()
	{

		if (wheel_status == WHEEL_INVISIBLE)
		{
			return "WHEEL_INVISIBLE";
		}
		else if (wheel_status == WHEEL_SETUP)
		{
			return "WHEEL_SETUP";
		}
		else if (wheel_status == WHEEL_VISIBLE)
		{

			return "WHEEL_VISIBLE";
		}
		else
		{
			return "Unknown wheel state";
		}
	}

	// handle the wheel mode button press (the right VR controller grip button)
	void handle_wheel_mode_button_timeout(bool everything_is_ready)
	{
		// If the right controller grip button is pressed,
		// and no button press timeout is going on...
		if (everything_is_ready && is_right_grip_down() && !wheel_mode_button_timeout)
		{
			// if no wheel mode button timeout is going on;
			// run the wheel mode handler function
			wheel_mode_button_timeout = true;

			/*

			Use static for timing or state management across multiple function calls
			where you want to keep track of a value between calls without re-initializing it.

			*/
			last_wheel_mode_press_time = steady_clock::now();

			handle_wheel_mode_button_press();

			// log_debug_message("Wheel mode button was clicked ! Current wheel mode is: %s \n", get_wheel_status_str());
			// log_debug_message("steam-vr-wheel center coordinates: x = %f , y = %f \n", wheel_center_position.x, wheel_center_position.y);
		}

		if (wheel_mode_button_timeout)
		{
			// Get the current time
			auto now = steady_clock::now();

			// Calculate the elapsed time since the last action
			auto elapsed = duration_cast<milliseconds>(now - last_wheel_mode_press_time).count();

			// Check if at least WHEEL_MODE_BUTTON_TIMEOUT_MSEC milliseconds has passed since the last action
			if (elapsed >= WHEEL_MODE_BUTTON_TIMEOUT_MSEC)
			{
				// indicate that there's no wheel button timeout
				wheel_mode_button_timeout = false;

				// log_debug_message("1 second has passed !");
			}
		}
	}

	// handle the wheel grab button (the left VR controller grip button)
	void handle_wheel_grab_button(
		bool everything_is_ready)
	{

		// If the left controller grip button is pressed and the wheel is visible...
		if (everything_is_ready && is_left_grip_down() && wheel_status == WHEEL_VISIBLE)
		{
			// 1) Set wheel_grabbed to true. This indicates that the wheel is currently being grabbed,
			// so now, steering will be applied in the on_get_xinput_state callback
			wheel_grabbed = true;
		}
		/* otherwise... */
		else
		{
			// 1) Set wheel_grabbed to false. This indicates that the wheel is not currently being grabbed,
			// or the wheel is currently invisible
			wheel_grabbed = false;
		}
	}

	// callback that handles the wheel mode button press
	// (the wheel mode button allows you to position the VR steering wheel)
	void handle_wheel_mode_button_press()
	{
		// contains the JSON object of the steam-vr-wheel options
		nlohmann::json steam_vr_wheel_options = getJSONObject(CONFIG_JSON_PATH);

		if (wheel_status == WHEEL_INVISIBLE)
		{

			// - set wheel_status to WHEEL_SETUP
			wheel_status = WHEEL_SETUP;

			// - set the edit_mode property of the JSON object in CONFIG_JSON_PATH to true
			steam_vr_wheel_options["edit_mode"] = true;

			// - set the wheel_degrees property of the JSON object in CONFIG_JSON_PATH to MAX_STEAM_VR_WHEEL_STEERING_ANGLE,
			steam_vr_wheel_options["wheel_degrees"] = MAX_STEAM_VR_WHEEL_STEERING_ANGLE;

			// - set the wheel_show_wheel property of the JSON object in CONFIG_JSON_PATH to true,
			steam_vr_wheel_options["wheel_show_wheel"] = true;

			// - set the wheel_show_hands property of the JSON object in CONFIG_JSON_PATH to true,
			steam_vr_wheel_options["wheel_show_hands"] = true;

			// - if steam_vr_wheel_started == false,
			// start the .bat file located at STEAM_VR_WHEEL_PATH (the wheel) ,
			// and set steam_vr_wheel_started to true
			if (steam_vr_wheel_started == false)
			{
				// runBatchFile(STEAM_VR_WHEEL_PATH);

				// steam_vr_wheel_started = true;
			}
		}
		else if (wheel_status == WHEEL_SETUP)
		{
			// - set wheel_status to WHEEL_VISIBLE
			wheel_status = WHEEL_VISIBLE;

			// - set the edit_mode property of the JSON object in CONFIG_JSON_PATH to false,
			steam_vr_wheel_options["edit_mode"] = false;

			// - set the wheel_show_wheel property of the JSON object in CONFIG_JSON_PATH to true,
			steam_vr_wheel_options["wheel_show_wheel"] = true;

			// - set the wheel_show_hands property of the JSON object in CONFIG_JSON_PATH to true,
			steam_vr_wheel_options["wheel_show_hands"] = true;

			// start the socket server on a separate thread
			start_socket_server();
		}
		else if (wheel_status == WHEEL_VISIBLE)
		{

			// - set wheel_status to WHEEL_INVISIBLE
			wheel_status = WHEEL_INVISIBLE;

			// - set the wheel_show_wheel property of the JSON object in CONFIG_JSON_PATH to false,
			steam_vr_wheel_options["wheel_show_wheel"] = false;

			// - set the wheel_show_hands property of the JSON object in CONFIG_JSON_PATH to false,
			steam_vr_wheel_options["wheel_show_hands"] = false;

			// stop the socket server thread
			stop_socket_server();
		}
		else
		{
			// - otherwise do nothing.
		}

		// save the steam-vr-wheel config edits
		setJSONObject(CONFIG_JSON_PATH, steam_vr_wheel_options);
	}

	// start the socket server on a separate thread
	void start_socket_server()
	{
		socket_server_thread = std::make_unique<std::jthread>([this](std::stop_token s)
															  { launch_socket_server(s); });
	}

	// stop the socket server thread
	void stop_socket_server()
	{
		if (socket_server_thread && socket_server_thread->joinable())
		{
			socket_server_thread->request_stop(); // Request thread to stop
			socket_server_thread->join();		  // Ensure thread joins

			log_debug_message("socket server/thread stopped !");
		}
	}

	// get the left and right VR controller position and rotation, and return true if success, or false otherwise
	bool get_controllers_positions_and_rotations(
		UEVR_Vector3f *left_position,
		UEVR_Vector3f *right_position,
		UEVR_Quaternionf *left_rotation,
		UEVR_Quaternionf *right_rotation)
	{
		const UEVR_VRData *vr = API::get()->param()->vr;
		// const auto runtime_is_ready = vr->is_runtime_ready();
		// const auto hmd_is_ready = vr->is_hmd_active();
		const auto controllers_are_ready = vr->is_using_controllers();
		const auto everything_is_ready = /*runtime_is_ready && hmd_is_ready &&*/ controllers_are_ready;

		if (!everything_is_ready)
			return false;

		vr->get_pose(vr->get_left_controller_index(), left_position, left_rotation);
		vr->get_pose(vr->get_right_controller_index(), right_position, right_rotation);

		return true;
	}

	// callback that gets executed right after the current tick
	void on_post_engine_tick(API::UGameEngine *engine, float delta) override {}

	// callback that allows you to programmatically press game buttonsn on every tick, thanks to the XINPUT API (state)
	void on_xinput_get_state(uint32_t *retval, uint32_t user_index, XINPUT_STATE *state) override
	{
		UEVR_Vector3f left_position;
		UEVR_Quaternionf left_rotation;
		UEVR_Vector3f right_position;
		UEVR_Quaternionf right_rotation;

		const auto everything_is_ready = get_controllers_positions_and_rotations(
			&left_position,
			&right_position,
			&left_rotation,
			&right_rotation);

		// #### On the on_xinput_get_state callback, do those things:

		// If wheel_grabbed is true,  programmatically push the left joystick to a desired position, based on total_steering_angle.
		if (everything_is_ready && wheel_grabbed && wheel_status == WHEEL_VISIBLE)
		{
			handle_steering(state);
		}
	}

	// Handles in-game steering, depending on the current VR steering wheel angle
	void handle_steering(
		XINPUT_STATE *state)
	{
		/*
		precise_steering_angle_degrees is the steering angle (in degrees) we get from steam-uevr-wheel.
		The angle value is negative when steering is clockwise, and postive when counterclockwise.
		We want the opposite, AKA positive clockwise and negative counterclockwise, because
		state->Gamepad.sThumbLX expects a positive clockwise and negative counterclockwise value .

		Let's flip the angle value and let's store this value in total_steering_angle_degrees
		*/
		float total_steering_angle_degrees = -precise_steering_angle_degrees;

		/*
		clamp total_steering_angle_degrees, so it ranges between -MAX_STEERING_ANGLE and MAX_STEERING_ANGLE.
		Store this clamped value in clamped_total_steering_angle.
		(MAX_STEERING_ANGLE is a defined constant whose value is 180.0f .
		MAX_STEERING_ANGLE degrees is the default maximum steering angle of our imaginary wheel)
		*/
		float clamped_total_steering_angle = std::max(-MAX_STEERING_ANGLE, std::min(MAX_STEERING_ANGLE, total_steering_angle_degrees));

		/*
		Then normalize clamped_total_steering_angle, between [-1.0 and 1.0] .
		Store this normalized value in normalized_total_steering_angle .
		*/
		float normalized_total_steering_angle = clamped_total_steering_angle / MAX_STEERING_ANGLE;

		/*
		Set total_joystick_push to normalized_total_steering_angle * 32767.f
		*/
		SHORT total_joystick_push = static_cast<SHORT>(normalized_total_steering_angle * 32767.f);

		/*
		Set sThumbLX, the left joystick X axis position to total_joystick_push
		(sThumbLX ranges from
		-32767.f (joystick pushed all the way to the left)
		to
		+32767.f (joystick pushed all the way to the right)
		*/
		state->Gamepad.sThumbLX = total_joystick_push;

		// print some shizzle, my nizzle ;-)
		// log_debug_message("ang: %f", total_steering_angle_degrees);
	}

	// Tells you if the left VR grip button is pressed
	bool is_left_grip_down()
	{
		const auto param = API::get()->param();
		const auto vr = param->vr;
		const auto left_joystick_source = vr->get_left_joystick_source();
		const auto grip_action = vr->get_action_handle("/actions/default/in/Grip");
		return vr->is_action_active(grip_action, left_joystick_source);
	}

	// Tells you if the right VR grip button is pressed
	bool is_right_grip_down()
	{
		const auto param = API::get()->param();
		const auto vr = param->vr;
		const auto right_joystick_source = vr->get_right_joystick_source();
		const auto grip_action = vr->get_action_handle("/actions/default/in/Grip");
		return vr->is_action_active(grip_action, right_joystick_source);
	}

	// Allows you to get the contents of the JSON file located at path
	nlohmann::json getJSONObject(const std::string &path)
	{
		nlohmann::json root;
		std::ifstream file_in(path);
		if (file_in.is_open())
		{
			file_in >> root;
			file_in.close();
		}
		else
		{
			log_debug_message("Unable to open JSON file for reading: ", path);
		}
		return root;
	}

	// Allows you to edit the contents of the JSON file located at path, with value
	void setJSONObject(const std::string &path, const nlohmann::json &value)
	{
		std::ofstream file_out(path, std::ofstream::trunc);
		if (file_out.is_open())
		{
			file_out << value.dump(4); // dump(4) to pretty-print with 4 spaces
			file_out.close();
		}
		else
		{
			log_debug_message("Unable to open JSON file for writing: ", path);
		}
	}

private:
	float precise_steering_angle_degrees;
	int wheel_status;
	bool wheel_grabbed;
	bool steam_vr_wheel_started;
	bool wheel_mode_button_timeout;
	std::unique_ptr<std::jthread> socket_server_thread;
	time_point<steady_clock> last_wheel_mode_press_time;
	PROCESS_INFORMATION wheel_process;
};

std::unique_ptr<VRHands> g_plugin{new VRHands()};
