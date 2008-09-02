
from core import *

if __name__ == '__main__' :
	
	_shell = Shell ()
	_view = View ()
	_handler = Handler ()
	
	_shell.set_view (_view)
	_shell.set_handler (_handler)
	_shell.open ()
	_shell.refresh ()
	_shell.input ('Hello?')
	_shell.close ()
