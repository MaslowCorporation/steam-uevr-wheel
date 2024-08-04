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


// the duration of the wheel mode button timeout in milliseconds
#define WHEEL_MODE_BUTTON_TIMEOUT_MSEC 1000

// PI is delicious ;-)
#define PI 3.14159265358979323846f

#include <zmq.hpp>
#include <boost/asio.hpp>
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
using boost::asio::ip::tcp;

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
				wheel_mode_button_timeout(false),
		        stop_zmq_server(false),
				MAX_STEERING_ANGLE_JSON(MAX_STEERING_ANGLE),
				MAX_STEAM_VR_WHEEL_STEERING_ANGLE_JSON(MAX_STEAM_VR_WHEEL_STEERING_ANGLE) {}

	// destructor function that runs when shizzle gets destroyed
	virtual ~VRHands()
	{
		// stop the .exe steam-uevr-wheel
		stop_exe_or_bat(wheel_process);

		// stop the socket server thread
		stop_socket_server();

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

		// create Documents/steam-uevr-wheel/config.json if needed.
		create_json_file_if_needed();

		// load the steering angles from the config.json object
		load_json_config_settings();

		// start the steam-uevr-wheel .exe file located in the Documents folder.
		start_steam_uevr_wheel_exe();

	}

	// closes a specific port
	void close_connection(tcp::socket& socket) {
		boost::system::error_code ec;
		socket.shutdown(tcp::socket::shutdown_both, ec);
		if (ec) {
			std::cerr << "Error shutting down socket: " << ec.message() << std::endl;
		}
		socket.close(ec);
		if (ec) {
			std::cerr << "Error closing socket: " << ec.message() << std::endl;
		}
	}

	// create Documents/steam-uevr-wheel/config.json if needed.
	void create_json_file_if_needed()
	{
		// path of the steam-uevr-wheel executable
		auto config_json_path_full = get_config_json_path();

		std::string config_json_path_full_str = config_json_path_full.string();

		// default JSON file content
		nlohmann::json json_data = nlohmann::json::object();

		json_data["MAX_STEERING_ANGLE"] = MAX_STEERING_ANGLE;
		json_data["MAX_STEAM_VR_WHEEL_STEERING_ANGLE"] = MAX_STEAM_VR_WHEEL_STEERING_ANGLE;

		create_json_file(config_json_path_full_str, json_data);
	}

	// load the steering angles from the config.json object
	void load_json_config_settings()
	{
		auto config_json_path_full = get_config_json_path();

		auto json_data = getJSONObject(config_json_path_full.string());

		MAX_STEERING_ANGLE_JSON = json_data["MAX_STEERING_ANGLE"];
		MAX_STEAM_VR_WHEEL_STEERING_ANGLE_JSON = json_data["MAX_STEAM_VR_WHEEL_STEERING_ANGLE"].get<int>();
	}

	// gets path of the config.json file (steam-uevr-wheel-cpp)
	std::filesystem::path get_config_json_path()
	{
		char *documents_folder_char = get_documents_folder();
		std::filesystem::path documents_folder(documents_folder_char);
		std::filesystem::path config_json_path = "steam-uevr-wheel-cpp\\config.json";
		std::filesystem::path config_json_path_full = documents_folder / config_json_path;

		return config_json_path_full;
	}

	// gets path of the config.json file (the one in AppData//Local/steam-vr-wheel)
	std::filesystem::path get_config_json_path_python()
	{
		char* user_folder_char = get_user_folder();
		std::filesystem::path user_folder(user_folder_char);
		std::filesystem::path config_json_path = "AppData\\Local\\steam-vr-wheel\\config.json";
		std::filesystem::path config_json_path_full = user_folder / config_json_path;

		return config_json_path_full;
	}

	// Function to get the path of the user's home folder on Windows
	char* get_user_folder()
	{
		PWSTR path = nullptr;
		HRESULT result = SHGetKnownFolderPath(FOLDERID_Profile, 0, nullptr, &path);
		static char buffer[MAX_PATH];

		if (SUCCEEDED(result))
		{
			// Convert from wide string to narrow string
			wcstombs(buffer, path, MAX_PATH);
			log_debug_message("User Folder Path: %s", buffer);
		}
		else
		{
			log_debug_message("Error: Unable to get the user folder path.");
			buffer[0] = '\0'; // Return an empty string on failure
		}

		// Free memory allocated by SHGetKnownFolderPath
		if (path)
		{
			CoTaskMemFree(path);
		}

		return buffer;
	}

	// start the steam-uevr-wheel .bat file located in the Documents folder.
	void start_steam_uevr_wheel_bat()
	{
		// path of the steam-uevr-wheel executable
		char *documents_folder_char = get_documents_folder();
		std::filesystem::path documents_folder(documents_folder_char);
		std::filesystem::path steam_uevr_bat_path = "steam-uevr-wheel\\steam-vr-wheel.bat";
		std::filesystem::path steam_uevr_folder_path = "steam-uevr-wheel";
		std::filesystem::path full_steam_uevr_bat_path = documents_folder / steam_uevr_bat_path;
		std::filesystem::path full_steam_uevr_folder_path = documents_folder / steam_uevr_folder_path;

		std::string full_steam_uevr_bat_path_str = full_steam_uevr_bat_path.string();
		std::string full_steam_uevr_folder_path_str = full_steam_uevr_folder_path.string();

		// log_debug_message("bat path: %s", full_steam_uevr_bat_path_str.c_str());
		// log_debug_message("steam-uevr-wheel folder path: %s", full_steam_uevr_folder_path_str.c_str());

		wheel_process = run_bat_file(full_steam_uevr_bat_path_str, full_steam_uevr_folder_path_str);
	}

	// starts the steam-uevr-wheel .exe
	void start_steam_uevr_wheel_exe()
	{
		// path of the steam-uevr-wheel executable
		char* documents_folder_char = get_documents_folder();
		std::filesystem::path documents_folder(documents_folder_char);
		std::filesystem::path steam_uevr_exe_path = "steam-uevr-wheel\\steam_vr_wheel_dist\\build\\exe.win-amd64-3.5\\open-vr-wheel.exe";
		std::filesystem::path full_steam_uevr_exe_path = documents_folder / steam_uevr_exe_path;




		std::string full_steam_uevr_exe_path_str = full_steam_uevr_exe_path.string();

		log_debug_message("steam-uevr-wheel exe path: %s", full_steam_uevr_exe_path_str.c_str());
		// log_debug_message("steam-uevr-wheel folder path: %s", full_steam_uevr_folder_path_str.c_str());

		wheel_process = start_exe(full_steam_uevr_exe_path);
	}

	// callback that handles hardware events (keyboard presses etc...)
	bool on_message(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam) override {
		if (msg == WM_KEYDOWN && wparam == VK_SHIFT) {
			handle_wheel_mode_button_press();

			log_debug_message("wheel mode is: %s \n", get_wheel_status_str());

			return false;
		}
	}

	// Helper function to convert std::string to LPWSTR
	LPWSTR stringToLPWSTR(const std::string &str)
	{
		int size_needed = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, nullptr, 0);
		LPWSTR lpwstr = new wchar_t[size_needed];
		MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, lpwstr, size_needed);
		return lpwstr;
	}

	// Function to run a .bat file with a specific working directory
	PROCESS_INFORMATION run_bat_file(const std::string &batFilePath, const std::string &workingDirectory)
	{
		// Convert std::string to LPWSTR for the .bat file path and working directory
		LPWSTR lpwstrFilePath = stringToLPWSTR(batFilePath);
		LPWSTR lpwstrWorkingDirectory = stringToLPWSTR(workingDirectory);

		// Initialize STARTUPINFO structure
		STARTUPINFO si = {0};
		si.cb = sizeof(si);
		PROCESS_INFORMATION pi = {0};

		// Create the command to run the .bat file
		std::wstring command = L"cmd.exe /c \"";
		command += lpwstrFilePath;
		command += L"\"";

		// Convert std::wstring to LPWSTR
		LPWSTR lpwstrCommand = new wchar_t[command.size() + 1];
		wcscpy_s(lpwstrCommand, command.size() + 1, command.c_str());

		// Start the process
		BOOL result = CreateProcess(
			nullptr,				// No module name (use command line)
			lpwstrCommand,			// Command line
			nullptr,				// Process handle not inheritable
			nullptr,				// Thread handle not inheritable
			FALSE,					// Set handle inheritance to FALSE
			0,						// No creation flags
			nullptr,				// Use parent's environment block
			lpwstrWorkingDirectory, // Use specified working directory
			&si,					// Pointer to STARTUPINFO structure
			&pi						// Pointer to PROCESS_INFORMATION structure
		);

		// Clean up allocated memory
		delete[] lpwstrFilePath;
		delete[] lpwstrCommand;
		delete[] lpwstrWorkingDirectory;

		if (!result)
		{
			log_debug_message("CreateProcess failed");
		}

		// Wait until the process finishes
		// WaitForSingleObject(pi.hProcess, INFINITE);

		// Close process and thread handles
		// CloseHandle(pi.hProcess);
		// CloseHandle(pi.hThread);

		return pi;
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

	// stop an .exe or .bat file from it's PROCESS_INFORMATION object
	BOOL stop_exe_or_bat(PROCESS_INFORMATION &processInfo)
	{

		if (processInfo.hProcess != nullptr)
		{
			BOOL result = TerminateProcess(processInfo.hProcess, 1); // Terminate process with exit code 1
			if (!result)
			{
				log_debug_message("TerminateProcess failed: %i", GetLastError());
				return false;
			}

			// Close process and thread handles
			CloseHandle(processInfo.hProcess);
			CloseHandle(processInfo.hThread);

			processInfo.hProcess = nullptr;
			processInfo.hThread = nullptr;

			return true;
		}
		else
		{
			log_debug_message("There's no .bat process to stop");
		}
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
	void launch_socket_server(std::stop_token s)
	{
		try
		{
			

			// Set up the IO context and acceptor
			boost::asio::io_context io_context;
			int sock_port = 65435;
			tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), sock_port));

			// Wait for a connection
			log_debug_message("Server listening on port %i...", sock_port);
			tcp::socket socket(io_context);
			acceptor.accept(socket);
			log_debug_message("Connection accepted!");

			// Prepare buffer for receiving a float (4 bytes)
			char buffer[sizeof(float)];


			while (!s.stop_requested())
			{
				boost::system::error_code error;

				// Read the data
				size_t length = boost::asio::read(socket, boost::asio::buffer(buffer), error);

				if (error == boost::asio::error::eof)
				{
					// Connection closed cleanly by peer.
					log_debug_message("Connection closed by client.");

					stop_socket_server();

					break;
				}
				else if (error)
				{
					throw boost::system::system_error(error); // Some other error.
				}

				if (length == sizeof(float))
				{
					// Convert bytes to float
					float received_float;
					std::memcpy(&received_float, buffer, sizeof(float));

					// log_debug_message("Received float: %f", received_float);

					precise_steering_angle_degrees = received_float;
				}
				else
				{
					log_debug_message("Received unexpected data size: %i bytes", length);
				}
			}
		}
		catch (std::exception &e)
		{
			stop_socket_server();

			log_debug_message("Exception: %s", e.what());
		}

	}


	// Function to launch ZeroMQ socket server
	void launch_socket_server_zmq(std::stop_token s)
	{
		int sock_port = 75832;

		zmq::context_t context(1);
		zmq::socket_t socket(context, zmq::socket_type::pull);

		const char* addr = "tcp://127.0.0.1:75832";

		try
		{
			
			socket.bind(addr);

			log_debug_message("ZMQ Server listening on %s...", addr);

			int timeout_counter = 0;
			const int max_timeouts = 5;

			while (!s.stop_requested()) {
				log_debug_message("Need to stop ?: %i", s.stop_requested());

				zmq::pollitem_t items[] = {
					{ static_cast<void*>(socket), 0, ZMQ_POLLIN, 0 }
				};

				zmq::poll(items, 1, std::chrono::milliseconds(1000)); // Poll with a timeout of 500 ms

				if (items[0].revents & ZMQ_POLLIN) {
					zmq::message_t request;
					if (socket.recv(request, zmq::recv_flags::none)) {
						if (request.size() == sizeof(float)) {
							// Convert bytes to float
							float received_float;
							std::memcpy(&received_float, request.data(), sizeof(float));

							// Process the received float
							precise_steering_angle_degrees = received_float;

							// Log the received float (optional)
							//log_debug_message("angle: %f", received_float);

							// Send an acknowledgment back to the client
							// zmq::message_t reply(5);
							// std::memcpy(reply.data(), "ACK", 4);
							// socket.send(reply, zmq::send_flags::none);
						}
						else {
							log_debug_message("Received unexpected data size: %zu bytes", request.size());

							// Send an error message back to the client
							// zmq::message_t reply(6);
							// std::memcpy(reply.data(), "ERROR", 6);
							// socket.send(reply, zmq::send_flags::none);
						}
					}
				}
				else {
					// Increment the counter on timeout
					timeout_counter++;
					if (timeout_counter >= max_timeouts) {
						log_debug_message("Reached maximum timeouts. Exiting loop.");
						break;
					}
				}

				// Additional non-blocking work can be done here
			}

			// stop the zmq server
			socket.unbind(addr);

			log_debug_message("ZMQ socket closed");


		}
		catch (const zmq::error_t& e)
		{
			log_debug_message("ZeroMQ Exception: %s", e.what());

			socket.unbind(addr);

		}
		catch (const std::exception& e)
		{
			log_debug_message("Exception: %s", e.what());

			socket.unbind(addr);

		}
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
		// path of the steam-uevr-wheel executable
		auto config_json_path_full = get_config_json_path_python();

		std::string config_json_path_full_str = config_json_path_full.string();

		// contains the JSON object of the steam-vr-wheel options
		nlohmann::json steam_vr_wheel_options = getJSONObject(config_json_path_full_str);

		// - set wheel_status to WHEEL_INVISIBLE
		wheel_status = WHEEL_INVISIBLE;

		// - set the wheel_show_wheel property of the JSON object in CONFIG_JSON_PATH to false,
		steam_vr_wheel_options["wheel_show_wheel"] = false;

		// - set the wheel_show_hands property of the JSON object in CONFIG_JSON_PATH to false,
		steam_vr_wheel_options["wheel_show_hands"] = false;

		// save the steam-vr-wheel config edits
		setJSONObject(config_json_path_full_str, steam_vr_wheel_options);
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
		// handle_wheel_mode_button_timeout(everything_is_ready);

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

			log_debug_message("wheel mode is: %s \n", get_wheel_status_str());
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
		if (everything_is_ready && (is_left_grip_down() || is_right_grip_down()) && wheel_status == WHEEL_VISIBLE)
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
		// path of the steam-uevr-wheel executable
		auto config_json_path_full = get_config_json_path_python();
		std::string config_json_path_full_str = config_json_path_full.string();

		// contains the JSON object of the steam-vr-wheel options
		nlohmann::json steam_vr_wheel_options = getJSONObject(config_json_path_full_str);

		if (wheel_status == WHEEL_INVISIBLE)
		{

			// - set wheel_status to WHEEL_SETUP
			wheel_status = WHEEL_SETUP;

			// - set the edit_mode property of the JSON object in CONFIG_JSON_PATH to true
			steam_vr_wheel_options["edit_mode"] = true;

			// - set the wheel_degrees property of the JSON object in CONFIG_JSON_PATH to MAX_STEAM_VR_WHEEL_STEERING_ANGLE_JSON,
			steam_vr_wheel_options["wheel_degrees"] = MAX_STEAM_VR_WHEEL_STEERING_ANGLE_JSON;

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
		setJSONObject(config_json_path_full_str, steam_vr_wheel_options);
	}

	// start the socket server on a separate thread
	void start_socket_server()
	{
		socket_server_thread = std::make_unique<std::jthread>([this](std::stop_token s)
															  { launch_socket_server_zmq(s); });
	}

	// stop the socket server thread
	bool stop_socket_server()
	{
		try {
			if (socket_server_thread)
			{
				log_debug_message("socket server/thread to be stopped !");

			    //stop_zmq_server = true;

				auto outcome_req = socket_server_thread->request_stop(); // Request thread to stop
				//socket_server_thread->join();		  // Ensure thread joins

				log_debug_message("socket server/thread stopping code %i", outcome_req);

				return true;
			}
			else {
				log_debug_message("No need to stop socket server/thread");

				return false;
			}
		}
		catch (const std::exception& e)
		{
			log_debug_message("Exception: %s", e.what());

			return false;
		
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
		clamp total_steering_angle_degrees, so it ranges between -MAX_STEERING_ANGLE_JSON and MAX_STEERING_ANGLE_JSON.
		Store this clamped value in clamped_total_steering_angle.
		(MAX_STEERING_ANGLE_JSON is a defined setting in config.json whose default value is 180.0f .
		MAX_STEERING_ANGLE degrees is the default maximum steering angle of our imaginary wheel)
		*/
		float clamped_total_steering_angle = std::max(-MAX_STEERING_ANGLE_JSON, std::min(MAX_STEERING_ANGLE_JSON, total_steering_angle_degrees));

		/*
		Then normalize clamped_total_steering_angle, between [-1.0 and 1.0] .
		Store this normalized value in normalized_total_steering_angle .
		*/
		float normalized_total_steering_angle = clamped_total_steering_angle / MAX_STEERING_ANGLE_JSON;

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
		std::ifstream ifs(path);
		nlohmann::json jf = nlohmann::json::parse(ifs);

		return jf;
	}

	// Allows you to edit the contents of the JSON file located at path, with value
	void setJSONObject(const std::string &path, const nlohmann::json &value)
	{
		std::ofstream file(path);

		// log_debug_message("JSON saved successfully: %s", value.dump().c_str());

		file << value;
	}

	// Function to create a JSON file with an empty JSON object if it does not already exist
	void create_json_file(const std::string &json_file, nlohmann::json json_data)
	{
		namespace fs = std::filesystem;

		// Check if the JSON file already exists
		if (fs::exists(json_file))
		{
			log_debug_message("JSON file already exists: %s", json_file.c_str());

			return; // Do nothing if the file exists
		}

		// Ensure that all directories in the path are created
		fs::path json_path = fs::path(json_file).parent_path();
		if (!json_path.empty() && !fs::exists(json_path))
		{
			if (!fs::create_directories(json_path))
			{
				log_debug_message("Failed to create directories for path: %s", json_path.string().c_str());
				return;
			}
		}

		// Create and write the empty JSON object to the file
		std::ofstream file_output(json_file);
		if (!file_output)
		{
			log_debug_message("Failed to create JSON file: %s", json_file.c_str());
			return;
		}

		file_output << json_data.dump(4); // Pretty print JSON with 4 spaces indentation
		file_output.close();

		log_debug_message("JSON file created successfully: %s", json_file.c_str());
	}

private:
	float precise_steering_angle_degrees;
	float MAX_STEERING_ANGLE_JSON;
	int MAX_STEAM_VR_WHEEL_STEERING_ANGLE_JSON;
	int wheel_status;
	bool wheel_grabbed;
	bool steam_vr_wheel_started;
	bool wheel_mode_button_timeout;
	bool stop_zmq_server;
	std::unique_ptr<std::jthread> socket_server_thread;
	time_point<steady_clock> last_wheel_mode_press_time;
	PROCESS_INFORMATION wheel_process;
	UEVR_Vector3f *cam_pos_setter;
};

std::unique_ptr<VRHands> g_plugin{new VRHands()};
