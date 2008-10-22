
'''
	SCE -- Simple Console Editor
	
	Copyright (C) 2008 Ciprian Dorin Craciun <ciprian.craciun@gmail.com>
	
	This file is part of the program SCE.
	
	The program is free software: you can redistribute it and / or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	
	The program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

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
	
	_handler.register_control ('@', mark_command)
	_handler.register_control ('G', go_command)
	_handler.register_control ('Z', jump_command)
	_handler.register_control ('V', jump_set_command)
	_handler.register_command ('mark', mark_command)
	_handler.register_command ('go', go_command)
	_handler.register_command ('gl', go_line_command)
	_handler.register_command ('gs', go_string_command)
	_handler.register_command ('jump', jump_command)
	_handler.register_command ('js', jump_set_command)
	
	_handler.register_control ('Y', yank_lines_command)
	_handler.register_control ('D', copy_lines_command)
	_handler.register_control ('K', cut_lines_command)
	_handler.register_command ('yank', yank_lines_command)
	_handler.register_command ('copy', copy_lines_command)
	_handler.register_command ('cut', cut_lines_command)
	_handler.register_command ('delete', delete_lines_command)
	
	_handler.register_control ('S', save_command)
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
	
	print
	if _error is not None :
		print
		print 'sce failed!'
		print
		print '----------------------------------------'
		print
		print _error[0]
		print _error[1]
		print '----------------------------------------'


if __name__ == '__main__' :
	sce (sys.argv[1 :])
