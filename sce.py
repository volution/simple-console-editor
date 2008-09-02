
from core import Shell
from sce_commands import *
from sce_handler import *
from sce_view import *


def sce (_arguments) :
	if len (_arguments) > 1 :
		print '[ee] sce: wrong syntax: sce [file]'
		return
	
	_view = View ()
	
	_handler = Handler ()
	
	_handler.register_control ('X', quick_exit_command)
	_handler.register_command ('exit', exit_command)
	_handler.register_command ('quick-exit', quick_exit_command)
	
	_handler.register_control ('R', _handler.handle_command)
	_handler.register_control ('G', go_command)
	
	_handler.register_control ('@', mark_command)
	_handler.register_command ('mark', mark_command)
	_handler.register_command ('go', go_command)
	
	_handler.register_control ('Y', yank_lines_command)
	_handler.register_control ('D', copy_lines_command)
	_handler.register_control ('K', cut_lines_command)
	_handler.register_command ('yank', yank_lines_command)
	_handler.register_command ('copy', copy_lines_command)
	_handler.register_command ('cut', cut_lines_command)
	_handler.register_command ('delete', delete_lines_command)
	
	_handler.register_command ('clear', clear_command)
	_handler.register_command ('open', open_command)
	_handler.register_command ('save', save_command)
	
	_handler.register_command ('load', load_command)
	_handler.register_command ('store', store_command)
	_handler.register_command ('sys', sys_command)
	_handler.register_command ('pipe', pipe_command)
	
	_shell = Shell ()
	_shell.set_view (_view)
	_shell.set_handler (_handler)
	
	_shell.open ()
	
	if len (_arguments) > 0 :
		open_command (_shell, [_arguments[0]])
	
	_error = _shell.loop ()
	
	_shell.close ()
	
	if _error is not None :
		print _error[0]
		print _error[1]
	print


if __name__ == '__main__' :
	sce (sys.argv[1 :])
