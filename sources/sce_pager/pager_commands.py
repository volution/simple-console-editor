
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *

__all__ = [
		
		"exit_command",
		"quick_exit_command",
		
		"mark_command",
		
		"jump_command",
		"jump_set_command",
		
		"go_command",
		"go_line_command",
		"go_string_command",
		"go_regexp_command",
		
		"load_command",
		"store_command",
		"load_fd_command",
		"store_fd_command",
		
		"filter_command",
		"select_highlight_command",
		"next_highlight_command",
	]


from sce_editor.editor_commands import \
		exit_command, quick_exit_command, \
		mark_command, \
		jump_command, jump_set_command, \
		go_command, go_line_command, go_string_command, go_regexp_command, \
		load_command, load_fd_command, \
		store_command, store_fd_command \
#


def filter_command (_shell, _arguments) :
	if len (_arguments) == 0 :
		_filter_re = None
		_filter_context = None
	elif len (_arguments) == 1 :
		_filter_re = _arguments[0]
		_filter_context = None
	elif len (_arguments) == 2 :
		_filter_re = _arguments[0]
		_filter_context = int (_arguments[1])
	else :
		_shell.notify ("filter: wrong syntax: filter <pattern> [<context>] | filter")
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_scroll.set_filter (_filter_re, _filter_context, _filter_context)
	return None


def select_highlight_command (_shell, _arguments, _delegate) :
	if len (_arguments) != 0 :
		_shell.notify ("output-highlight: wrong syntax: output-highlight")
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_line = _cursor.get_line ()
	_column = _view.select_real_column (_line, _cursor.get_column ())
	_highlights = _scroll.highlights (_line)
	if _highlights is not None :
		_found = False
		for _highlight in _scroll.highlights (_line) :
			if _column >= _highlight[0] and _column <= _highlight[1] :
				_found = True
		if not _found :
			_highlight = None
	if _highlight is None :
		_shell.notify ("output-highlight: no match selected")
		return None
	return _delegate (_shell, _line, _highlight)


def next_highlight_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ("next-highlight: wrong syntax: next-highlight")
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_lines = _view.get_lines ()
	_cursor = _view.get_cursor ()
	if _lines == 0 :
		return True
	_line = _cursor.get_line ()
	_column = _view.select_real_column (_line, _cursor.get_column ()) + 1
	_found = False
	for _line in itertools.chain (xrange_ (_line, _lines), xrange_ (0, _line)) :
		_found = False
		for _highlight in _scroll.highlights (_line) :
			if _column <= _highlight[0] :
				_column = _highlight[0]
				_found = True
				break
		if _found :
			break
		_column = -1
	if _found :
		_cursor.set_line (_line)
		_cursor.set_column (_view.select_visual_column (_line, _column))
	else :
		_shell.notify ("next-highlight: no match found")
	return True

