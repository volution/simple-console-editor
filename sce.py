
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


import os
import sys
import uuid

from core import Shell
from sce_commands import *
from sce_handler import *
from sce_view import *


def sce (_arguments) :
	
	if not os.isatty (2) :
		return False
	
	_redirected_input = None
	if not os.isatty (0) :
		_redirected_input = os.dup (0)
		os.dup2 (2, 0)
	
	_redirected_output = None
	if not os.isatty (1) :
		_redirected_output = os.dup (1)
		os.dup2 (2, 1)
	
	_shell = _create ()
	if _shell is None :
		return False
	
	if _redirected_input is None and _redirected_output is None :
		if len (_arguments) > 0 :
			_load = lambda : open_command (_shell, _arguments)
		else :
			_load = lambda : True
		_store = lambda : True
	else :
		if _redirected_input is not None :
			_load = lambda : load_fd_command (_shell, [], _redirected_input)
		else :
			_load = lambda : True
		if _redirected_output is not None :
			_store = lambda : store_fd_command (_shell, [], _redirected_output)
		else :
			_store = lambda : True
	
	if not _load () :
		return False
	
	_error = _loop (_shell)
	if _error is not None :
		print _error[1]
		try :
			_dump_path = "/tmp/sce.%d.dump.%s" % (os.getuid (), uuid.uuid4 () .hex)
			_dump_stream = os.open (_dump_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC)
			if not store_fd_command (_shell, [], _dump_stream) :
				raise Exception ()
			print >> sys.stderr, '[ee]', 'dumpped to %s' % (_dump_path,)
		except :
			print >> sys.stderr, '[ee]', 'dump failed!'
		return _error
	
	if not _store () :
		return False
	
	return None


def _loop (_shell) :
	
	_error = _shell.open ()
	if _error is not None :
		return _error
	
	_error = _shell.loop ()
	if _error is not None :
		_shell.close ()
		return _error
	
	_error = _shell.close ()
	if _error is not None :
		return _error
	
	return None


def _create () :
	
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
	_handler.register_command ('gr', go_regexp_command)
	_handler.register_command ('jump', jump_command)
	_handler.register_command ('js', jump_set_command)
	
	_handler.register_control ('Y', yank_lines_command)
	_handler.register_control ('D', copy_lines_command)
	_handler.register_control ('K', cut_lines_command)
	_handler.register_command ('yank', yank_lines_command)
	_handler.register_command ('copy', copy_lines_command)
	_handler.register_command ('cut', cut_lines_command)
	_handler.register_command ('delete', delete_lines_command)
	
	_handler.register_control ('N', replace_command)
	_handler.register_command ('replace', replace_command)
	
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
	
	return _shell


if __name__ == '__main__' :
	_error = sce (sys.argv[1 :])
	if _error is not None :
		print >> sys.stderr, '[ee]', 'failed!'
		sys.exit (1)
	else :
		sys.exit (0)
