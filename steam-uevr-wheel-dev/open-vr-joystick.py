import steam_vr_wheel
import steam_vr_wheel.wheel
import openvr
if __name__ == '__main__':
	try:
		steam_vr_wheel.wheel.main('joystick')
	except (Exception, openvr.OpenVRError) as e:
		import traceback
		traceback.print_exc()
		input()
		
