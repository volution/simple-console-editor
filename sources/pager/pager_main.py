
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

from core import *
from common import *
from pager_commands import *
from pager_handler import *
from pager_scroll import *


def main (_arguments) :
	
	if len (_arguments) != 0 :
		return False
	
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
	
	_scroll = _shell.get_view () .get_scroll ()
	
	if _redirected_input is None :
		return False
	
	if not load_fd_command (_shell, [], _redirected_input) :
		return False
	
	_scroll.reset_touched ()
	
	_scroll.set_highlights ("^[ ]*([0-9]+)", "\\g<0>", "\\g<1>")
	
	_error = _loop (_shell)
	if _error is not None :
		print _error[1]
		return _error
	
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
	
	_scroll = Scroll ()
	
	_view = View ()
	_view.set_scroll (_scroll)
	
	_handler = Handler ()
	
	_handler.register_control ('X', quick_exit_command)
	_handler.register_command ('exit', exit_command)
	_handler.register_command ('quick-exit', quick_exit_command)
	
	_handler.register_control ('R', lambda _shell, _arguments : _handler.handle_command (_shell))
	
	_handler.register_special ('Enter', output_highlight_data_command)
	_handler.register_special ('Tab', next_highlight_command)
	
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
	
	_handler.register_command ('store', store_command)
	
	_shell = Shell ()
	_shell.set_view (_view)
	_shell.set_handler (_handler)
	
	return _shell
