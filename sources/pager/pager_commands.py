

import itertools


from editor.editor_commands import \
		exit_command, quick_exit_command, \
		mark_command, \
		store_command, load_fd_command, \
		go_command, go_line_command, go_string_command, \
		jump_command, jump_set_command


def filter_command (_shell, _arguments) :
	if len (_arguments) == 0 :
		_filter = None
	elif len (_arguments) == 1 :
		_filter = _arguments[0]
	else :
		_shell.notify ('filter: wrong syntax: filter <pattern> | filter')
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_scroll.set_filter (_filter)
	return None

def output_highlight_data_command (_shell, _arguments, _delegate) :
	if len (_arguments) != 0 :
		_shell.notify ('output-highlight: wrong syntax: output-highlight')
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	_cursor_column = _cursor.get_column ()
	_highlight = _scroll.highlight (_cursor_line, _cursor_column)
	if _highlight is None :
		_shell.notify ('output-highlight: no match selected')
		return None
	return _delegate (_highlight[3])


def next_highlight_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('next-highlight: wrong syntax: next-highlight')
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
	for _line in itertools.chain (xrange (_line, _lines), xrange (0, _line)) :
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
		_shell.notify ('next-highlight: no match found')
	return True
