import steam_vr_wheel.configurator
if __name__ == '__main__':
	try:
		steam_vr_wheel.configurator.run()
	except Exception as e:
		import traceback
		traceback.print_exc()
		input()
		
