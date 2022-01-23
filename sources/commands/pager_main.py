
if __name__ == "__main__" :
	
	import sys, os
	if "SCE_SOURCES" in os.environ :
		sys.path.append (os.environ["SCE_SOURCES"])
	
	import pager, commands
	commands.main (pager.main)
	raise Exception ("6e701fee")
	
else :
	raise Exception ("dcbee9f0")

