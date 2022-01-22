
if __name__ == '__main__' :
	
	import sys, os
	sys.path.append (os.environ['SCE_SOURCES'])
	
	import pager, commands
	commands.main (pager.main)
	raise Exception ('566b6ea5')
	
else :
	raise Exception ('4f67e656')

