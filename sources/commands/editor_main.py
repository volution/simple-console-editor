

if __name__ == "__main__" :
	
	import sys, os
	if "SCE_SOURCES" in os.environ :
		sys.path.append (os.environ["SCE_SOURCES"])
	
	import editor, commands
	commands.main (editor.main)
	raise Exception ("566b6ea5")
	
else :
	raise Exception ("4f67e656")

