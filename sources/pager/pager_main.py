
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import os
import sys
import uuid

from core import *
from common import *

from .pager_commands import *
from .pager_handler import *
from .pager_scroll import *


def main (_arguments, _terminal, _transcript) :
	
	if len (_arguments) == 0 :
		_highlight_re = "^.*$"
		_highlight_strings_sub = ("", "-- ", "\\g<0>")
		_highlight_data_sub = "\\g<0>"
	elif len (_arguments) == 1 :
		_highlight_re = _arguments[0]
		_highlight_strings_sub = ("", "\\g<0>", "")
		_highlight_data_sub = "\\g<0>"
	elif len (_arguments) == 5 :
		_highlight_re = _arguments[0]
		_highlight_strings_sub = (_arguments[1], _arguments[2], _arguments[3])
		_highlight_data_sub = _arguments[4]
	else :
		_transcript.error ("invalid arguments;  expected: [<pattern> [<display-prefix> <display-anchor> <display-suffix> <output>]];  aborting!")
		return False
	
	_multiple_selection = True
	
	_filter_re = None
	_filter_context = None
	
	_redirected_input = None
	if not os.isatty (0) :
		_redirected_input = os.dup (0)
	
	_redirected_output = None
	if not os.isatty (1) :
		_redirected_output = os.dup (1)
	
	if _redirected_input is None :
		_transcript.error ("invalid standard input;  expected a non-TTY;  aborting!")
		return False
	
	if _redirected_output is None :
		_transcript.error ("invalid standard output;  expected a non-TTY;  aborting!")
		return False
	
	_selection = set ()
	def _highlight_select (_shell, _line, _highlight) :
		_selected = _highlight[3]
		_shell.get_view () .get_scroll () .flush_highlights_classifier ()
		if _selected not in _selection :
			_selection.add (_selected)
		else :
			_selection.remove (_selected)
		if len (_selection) > 0 and not _multiple_selection :
			_shell.loop_stop ()
		return None
	
	def _highlight_classify (_line, _anchor_begin, _anchor_end, _anchor, _data) :
		if _data in _selection :
			return 2
		else :
			return 1
	
	_shell = _initialize (_terminal, _highlight_select)
	if _shell is None :
		return False
	
	_scroll = _shell.get_view () .get_scroll ()
	
	if not load_fd_command (_shell, [], _redirected_input) :
		return False
	
	_scroll.reset_touched ()
	_scroll.seal ()
	
	_scroll.set_filter (_filter_re, _filter_context, _filter_context)
	_scroll.set_highlights (_highlight_re, _highlight_strings_sub, _highlight_data_sub)
	_scroll.set_highlights_classifier (_highlight_classify)
	
	_error = _loop (_shell)
	if _error is not None :
		return _error
	
	if len (_selection) > 0 :
		for _selected in sorted (_selection) :
			os.write (_redirected_output, _selected + "\n")
		return True
	else :
		return False


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


def _initialize (_terminal, _highlight_select) :
	
	_scroll = Scroll ()
	
	_view = View ()
	_view.set_scroll (_scroll)
	
	_handler = Handler ()
	
	_handler.register_control ("X", quick_exit_command)
	_handler.register_command ("exit", exit_command)
	_handler.register_command ("quick-exit", quick_exit_command)
	
	_handler.register_command ("filter", filter_command)
	
	_handler.register_control ("R", lambda _shell, _arguments : _handler.handle_command (_shell))
	
	_handler.register_special ("Enter", lambda _shell, _arguments : select_highlight_command (_shell, _arguments, _highlight_select))
	_handler.register_special ("Tab", next_highlight_command)
	
	_handler.register_control ("@", mark_command)
	_handler.register_control ("G", go_command)
	_handler.register_control ("Z", jump_command)
	_handler.register_control ("V", jump_set_command)
	_handler.register_command ("mark", mark_command)
	_handler.register_command ("go", go_command)
	_handler.register_command ("gl", go_line_command)
	_handler.register_command ("gs", go_string_command)
	_handler.register_command ("jump", jump_command)
	_handler.register_command ("js", jump_set_command)
	
	_handler.register_command ("store", store_command)
	
	_shell = Shell ()
	_shell.set_view (_view)
	_shell.set_handler (_handler)
	_shell.set_terminal (_terminal)
	
	return _shell

