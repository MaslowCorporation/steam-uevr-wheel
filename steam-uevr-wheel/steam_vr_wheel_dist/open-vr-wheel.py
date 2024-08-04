import steam_vr_wheel
import steam_vr_wheel.wheel
import openvr

import os
import json


if __name__ == '__main__':
	try:
		# Update JSON file to indicate script is running
		steam_vr_wheel.wheel.main()
	except (Exception, openvr.OpenVRError) as e:
		# Update JSON file to indicate script has stopped running

		import traceback
		traceback.print_exc()
		input()

		print("Bye ;-)")	
	finally:
        # Update JSON file to indicate script has stopped running
		print("Bye ;-)")	
