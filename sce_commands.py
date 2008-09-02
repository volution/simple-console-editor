
import codecs
import os.path
import subprocess
import sys


def exit_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('exit: wrong syntax: exit')
		return
	_shell.loop_stop ()


def mark_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('mark: wrong syntax: mark')
		return
	_view = _shell.get_view ()
	if _view.is_mark_enabled () :
		_view.set_mark_enabled (False)
	else :
		_cursor = _view.get_cursor ()
		_mark = _view.get_mark ()
		_view.set_mark_enabled (True)
		_mark.set_line (_cursor.get_line ())
		_mark.set_column (_cursor.get_column ())


def clear_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('clear: wrong syntax: clear')
		return
	_shell.get_view () .get_scroll () .empty ()


_yank_buffer = None


def yank_lines_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('yank-lines: wrong syntex: yank-lines')
		return
	if _yank_buffer is None :
		_shell.notify ('yank-lines: yank buffer is empty.')
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	if isinstance(_yank_buffer, list) :
		_scroll.include_all_before (_cursor_line, _yank_buffer)
	else :
		_visual_column = _cursor.get_column ()
		_real_column = _view.select_real_column (_cursor_line, _visual_column)
		_scroll.insert (_cursor_line, _real_column, _yank_buffer)
		_cursor.set_column (_view.select_visual_column (_cursor_line, _real_column + len (_yank_buffer)))


def copy_lines_command (_shell, _arguments) :
	global _yank_buffer
	if len (_arguments) != 0 :
		_shell.notify ('copy-lines: wrong syntax: copy-lines')
		return
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	if _view.is_mark_enabled () :
		_mark = _view.get_mark ()
		_mark_line = _mark.get_line ()
		if _mark_line == _cursor_line :
			_cursor_real_column = _view.select_real_column (_cursor_line, _cursor.get_column ())
			_mark_real_column = _view.select_real_column (_cursor_line, _mark.get_column ())
			_first_real_column = min (_mark_real_column, _cursor_real_column)
			_last_real_column = max (_mark_real_column, _cursor_real_column)
			_string = _scroll.select (_cursor_line)
			_yank_buffer = _string[_first_real_column : _last_real_column]
		else :
			_first_line = min (_mark_line, _cursor_line)
			_last_line = max (_mark_line, _cursor_line)
			_yank_buffer = []
			for _line in xrange (_first_line, _last_line + 1) :
				_yank_buffer.append (_scroll.select (_line))
		_view.set_mark_enabled (False)
	else :
		_yank_buffer = [_scroll.select (_cursor_line)]


def delete_lines_command (_shell, _arguments) :
	global _yank_buffer
	if len (_arguments) != 0 :
		_shell.notify ('delete-lines: wrong syntax: delete-lines')
		return
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	if _view.is_mark_enabled () :
		_mark = _view.get_mark ()
		_mark_line = _mark.get_line ()
		if _mark_line == _cursor_line :
			_cursor_real_column = _view.select_real_column (_cursor_line, _cursor.get_column ())
			_mark_real_column = _view.select_real_column (_cursor_line, _mark.get_column ())
			_first_real_column = min (_mark_real_column, _cursor_real_column)
			_last_real_column = max (_mark_real_column, _cursor_real_column)
			_string = _scroll.select (_cursor_line)
			_yank_buffer = _string[_first_real_column : _last_real_column]
			_scroll.delete (_cursor_line, _first_real_column, _last_real_column - _first_real_column)
			_cursor.set_column (_view.select_visual_column (_cursor_line, _first_real_column))
		else :
			_first_line = min (_mark_line, _cursor_line)
			_last_line = max (_mark_line, _cursor_line)
			_yank_buffer = []
			for _line in xrange (_first_line, _last_line + 1) :
				_yank_buffer.append (_scroll.select (_first_line))
				_scroll.exclude (_first_line)
			_cursor.set_line (_first_line)
		_view.set_mark_enabled (False)
	else :
		_yank_buffer = [_scroll.select (_cursor_line)]
		_scroll.exclude (_cursor_line)


def load_command (_shell, _arguments) :
	if len (_arguments) != 2 :
		_shell.notify ('load: wrong syntax: load r|i|a <file>')
		return
	_mode = _arguments[0]
	_path = _arguments[1]
	if _mode not in ['r', 'i', 'a'] :
		_shell.notify ('load: wrong mode (r|i|a); aborting.')
		return
	if not os.path.isfile (_path) :
		_shell.notify ('load: target file does not exist; aborting.')
		return
	try :
		_stream = codecs.open (_path, 'r', 'utf-8')
		_lines = _stream.readlines ()
		_stream.close ()
	except :
		_shell.notify ('load: input failed; aborting.')
		if _stream is not None :
			_stream.close ()
		return
	_load_file_lines (_shell, _mode, _lines)
	return True


def sys_command (_shell, _arguments) :
	if len (_arguments) < 2 :
		_shell.notify ('sys: wrong syntax: sys r|i|a <command> <argument> ...')
		return
	_mode = _arguments[0]
	_system_arguments = _arguments[1 :]
	if _mode not in ['r', 'i', 'a'] :
		_shell.notify ('sys: wrong mode (r|i|a); aborting.')
		return
	_shell.hide ()
	try :
		_process = subprocess.Popen (
				_system_arguments, shell = False, env = None,
				stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
				bufsize = 1, close_fds = True, universal_newlines = True)
	except :
		_shell.show ()
		_shell.notify ('sys: spawn failed; aborting.')
		return
	try :
		_stream = codecs.EncodedFile (_process.stdout, 'utf-8')
		_lines = _stream.readlines ()
		_stream.close ()
		_stream = codecs.EncodedFile (_process.stderr, 'utf-8')
		_error_lines = _stream.readlines ()
		_stream.close ()
		_error = _process.wait ()
	except :
		_shell.show ()
		_shell.notify ('sys: input failed; aborting.')
		return
	_shell.show ()
	if _error != 0 :
		_shell.notify ('sys: command failed (non zero exit code); ignoring.')
	if len (_error_lines) != 0 :
		for _line in _error_lines :
			_line = _line.rstrip ('\r\n')
			_shell.notify ('sys: %s', _line)
	_load_file_lines (_shell, _mode, _lines)


def pipe_command (_shell, _arguments) :
	if len (_arguments) < 1 :
		_shell.notify ('pipe: wrong syntax: pipe <command> <arguments> ...')
		return
	_system_arguments = _arguments
	try :
		_process = subprocess.Popen (
				_system_arguments, shell = False, env = None,
				stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
				bufsize = 1, close_fds = True, universal_newlines = True)
	except :
		_shell.notify ('pipe: spawn failed; aborting.')
		return
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	_lines = []
	if _view.is_mark_enabled () :
		_mark = _view.get_mark ()
		_mark_line = _mark.get_line ()
		_first_line = min (_mark_line, _cursor_line)
		_last_line = max (_mark_line, _cursor_line)
	else :
		_first_line = 0
		_last_line = _scroll.get_length () - 1
	for _line in xrange (_first_line, _last_line + 1) :
		_lines.append (_scroll.select (_line))
	try :
		_stream = codecs.EncodedFile (_process.stdin, 'utf-8')
		for _line in _lines :
			_stream.write (_line)
			_stream.write ('\n')
		_stream.close ()
		_stream = codecs.EncodedFile (_process.stdout, 'utf-8')
		_lines = _stream.readlines ()
		_stream.close ()
		_stream = codecs.EncodedFile (_process.stderr, 'utf-8')
		_error_lines = _stream.readlines ()
		_stream.close ()
		_error = _process.wait ()
	except :
		_shell.notify ('pipe: input failed; aborting.')
		return
	if _error != 0 :
		_shell.notify ('sys: command failed (non zero exit code); ignoring.')
	if len (_error_lines) != 0 :
		for _line in _error_lines :
			_line = _line.rstrip ('\r\n')
			_shell.notify ('sys: %s', _line)
	for _line in xrange (_first_line, _last_line + 1) :
		_scroll.exclude (_first_line)
	for _line in _lines :
		_line = _line.rstrip ('\r\n')
		_scroll.include_before (_first_line, _line)
	if _view.is_mark_enabled () :
		if len (_lines) == 0 :
			_view.set_mark_enabled (False)
		else :
			_last_line = _first_line + len (_lines) - 1
			_cursor.set_line (_first_line)
			_mark.set_line (_last_line)


def _load_file_lines (_shell, _mode, _lines) :
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	if _mode == 'r' :
		_scroll.empty ()
		_insert_line = 0
	elif _mode == 'i' :
		_insert_line = _view.get_cursor () .get_line ()
	elif _mode == 'a' :
		_insert_line = _scroll.get_length ()
	else :
		_insert_line = _scroll.get_length ()
	_lines.reverse ()
	for _line in _lines :
		_line = _line.rstrip ('\r\n')
		_scroll.include_before (_insert_line, _line)


def store_command (_shell, _arguments) :
	if len (_arguments) != 3 :
		_shell.notify ('store: wrong syntax: store a|t o|c <file>')
		return
	_selector = _arguments[0]
	_mode = _arguments[1]
	_path = _arguments[2]
	if _selector not in ['a', 't'] :
		_shell.notify ('store: wrong selector (a|t); aborting.')
		return
	if _mode not in ['o', 'c'] :
		_shell.notify ('store: wrong mode (o|c); aborting.')
		return
	if _mode == 'c' and os.path.isfile (_path) :
		_shell.notify ('store: target file exists; aborting.')
		return
	try :
		_stream = codecs.open (_path, 'w', 'utf-8')
		_view = _shell.get_view ()
		_lines = _view.get_lines ()
		for _line in xrange (0, _lines) :
			if _selector == 'a' or _view.select_is_tagged (_line) :
				_string = _view.select_real_string (_line)
				_stream.write (_string)
				_stream.write ('\n')
		_stream.close ()
	except :
		_shell.notify ('store: output failed; target file might have been destroyed!')
		return


def open_command (_shell, _arguments) :
	if len (_arguments) != 1 :
		_shell.notify ('open: wrong syntax: open <file>')
		return
	_path = _arguments[0]
	_succeeded = load_command (_shell, ['r', _path])
	if _succeeded :
		_shell.get_view () ._open_command_path = _path


def save_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('save: wrong syntax: save')
		return
	_path = _shell.get_view () ._open_command_path
	if _path is None :
		_shell.notify ('save: no previous open command; aborting.')
		return
	_succeeded = store_command (_shell, ['a', 'o', _path])
