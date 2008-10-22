
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

import codecs
import os.path
import subprocess
import sys


def exit_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('exit: wrong syntax: exit')
		return None
	_shell.loop_stop ()
	return True


def quick_exit_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('quick-exit: wrong syntax: quick-exit')
		return None
	if _shell.get_view () .get_scroll () .is_touched () :
		_shell.notify ('quick-exit: scroll is touched; aborting.')
		return None
	return exit_command (_shell, [])


def mark_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('mark: wrong syntax: mark')
		return None
	_view = _shell.get_view ()
	if _view.is_mark_enabled () :
		_view.set_mark_enabled (False)
	else :
		_cursor = _view.get_cursor ()
		_mark = _view.get_mark ()
		_view.set_mark_enabled (True)
		_mark.set_line (_cursor.get_line ())
		_mark.set_column (_cursor.get_column ())
	return True


def clear_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('clear: wrong syntax: clear')
		return None
	_shell.get_view () .get_scroll () .exclude_all ()
	return True


_yank_buffer = None


def yank_lines_command (_shell, _arguments) :
	global _yank_buffer
	if len (_arguments) != 0 :
		_shell.notify ('yank-lines: wrong syntex: yank-lines')
		return None
	if _yank_buffer is None :
		_shell.notify ('yank-lines: yank buffer is empty.')
		return None
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	if isinstance (_yank_buffer, list) :
		_scroll.include_all_before (_cursor_line, _yank_buffer)
	else :
		_visual_column = _cursor.get_column ()
		_real_column = _view.select_real_column (_cursor_line, _visual_column)
		_scroll.insert (_cursor_line, _real_column, _yank_buffer)
		_cursor.set_column (_view.select_visual_column (_cursor_line, _real_column + len (_yank_buffer)))
	return True


def copy_lines_command (_shell, _arguments) :
	if _copy_lines (_shell, _arguments) is None :
		return None
	_view = _shell.get_view ()
	if _view.is_mark_enabled () :
		_view.set_mark_enabled (False)
	return True


def _copy_lines (_shell, _arguments) :
	global _yank_buffer
	if len (_arguments) != 0 :
		_shell.notify ('copy-lines: wrong syntax: copy-lines')
		return None
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
	else :
		_yank_buffer = [_scroll.select (_cursor_line)]
	return True


def delete_lines_command (_shell, _arguments) :
	if _delete_lines (_shell, _arguments) is None :
		return None
	_view = _shell.get_view ()
	if _view.is_mark_enabled () :
		_view.set_mark_enabled (False)
	return True


def _delete_lines (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('delete-lines: wrong syntax: delete-lines')
		return None
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
			_scroll.delete (_cursor_line, _first_real_column, _last_real_column - _first_real_column)
			_cursor.set_column (_view.select_visual_column (_cursor_line, _first_real_column))
		else :
			_first_line = min (_mark_line, _cursor_line)
			_last_line = max (_mark_line, _cursor_line)
			for _line in xrange (_first_line, _last_line + 1) :
				_scroll.exclude (_first_line)
			_cursor.set_line (_first_line)
	else :
		_scroll.exclude (_cursor_line)
	return True


def cut_lines_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('cut-lines: wrong syntax: cut-lines')
		return None
	if _copy_lines (_shell, []) is None :
		return None
	if _delete_lines (_shell, []) is None :
		return None
	_view = _shell.get_view ()
	if _view.is_mark_enabled () :
		_view.set_mark_enabled (False)
	return True


def load_command (_shell, _arguments) :
	if len (_arguments) != 2 :
		_shell.notify ('load: wrong syntax: load r|i|a <file>')
		return None
	_mode = _arguments[0]
	_path = _arguments[1]
	if _mode not in ['r', 'i', 'a'] :
		_shell.notify ('load: wrong mode (r|i|a); aborting.')
		return None
	if not os.path.isfile (_path) :
		_shell.notify ('load: target file does not exist; aborting.')
		return None
	try :
		_stream = codecs.open (_path, 'r', 'utf-8')
		_lines = _stream.readlines ()
		_stream.close ()
	except :
		_shell.notify ('load: input failed; aborting.')
		if _stream is not None :
			_stream.close ()
		return None
	return _load_file_lines (_shell, _mode, _lines)


def sys_command (_shell, _arguments) :
	if len (_arguments) < 2 :
		_shell.notify ('sys: wrong syntax: sys r|i|a <command> <argument> ...')
		return None
	_mode = _arguments[0]
	_system_arguments = _arguments[1 :]
	if _mode not in ['r', 'i', 'a'] :
		_shell.notify ('sys: wrong mode (r|i|a); aborting.')
		return None
	_shell.close ()
	try :
		_process = subprocess.Popen (
				_system_arguments, shell = False, env = None,
				stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
				bufsize = 1, close_fds = True, universal_newlines = True)
	except :
		_shell.open ()
		_shell.notify ('sys: spawn failed; aborting.')
		return None
	try :
		_stream = codecs.EncodedFile (_process.stdout, 'utf-8')
		_lines = _stream.readlines ()
		_stream.close ()
		_stream = codecs.EncodedFile (_process.stderr, 'utf-8')
		_error_lines = _stream.readlines ()
		_stream.close ()
		_error = _process.wait ()
	except :
		_shell.open ()
		_shell.notify ('sys: input failed; aborting.')
		return None
	_shell.open ()
	if _error != 0 :
		_shell.notify ('sys: command failed (non zero exit code); ignoring.')
	if len (_error_lines) != 0 :
		for _line in _error_lines :
			_line = _line.rstrip ('\r\n')
			_shell.notify ('sys: %s', _line)
	return _load_file_lines (_shell, _mode, _lines)


def pipe_command (_shell, _arguments) :
	if len (_arguments) < 1 :
		_shell.notify ('pipe: wrong syntax: pipe <command> <arguments> ...')
		return None
	_system_arguments = _arguments
	try :
		_process = subprocess.Popen (
				_system_arguments, shell = False, env = None,
				stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
				bufsize = 1, close_fds = True, universal_newlines = True)
	except :
		_shell.notify ('pipe: spawn failed; aborting.')
		return None
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
	return True


def _load_file_lines (_shell, _mode, _lines) :
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	if _mode == 'r' :
		_scroll.exclude_all ()
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
	return True


def store_command (_shell, _arguments) :
	if len (_arguments) != 3 :
		_shell.notify ('store: wrong syntax: store a|t o|c <file>')
		return None
	_selector = _arguments[0]
	_mode = _arguments[1]
	_path = _arguments[2]
	if _selector not in ['a', 't'] :
		_shell.notify ('store: wrong selector (a|t); aborting.')
		return None
	if _mode not in ['o', 'c'] :
		_shell.notify ('store: wrong mode (o|c); aborting.')
		return None
	if _mode == 'c' and os.path.isfile (_path) :
		_shell.notify ('store: target file exists; aborting.')
		return None
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
		return None
	return True


_open_path = None


def open_command (_shell, _arguments) :
	global _open_path
	if len (_arguments) != 1 :
		_shell.notify ('open: wrong syntax: open <file>')
		return None
	_path = _arguments[0]
	if load_command (_shell, ['r', _path]) is None :
		return None
	_open_path = _path
	_shell.get_view () .get_scroll () .reset_touched ()
	return True


def save_command (_shell, _arguments) :
	global _open_path
	if len (_arguments) != 0 :
		_shell.notify ('save: wrong syntax: save')
		return None
	_path = _open_path
	if _path is None :
		_shell.notify ('save: no previous open command; aborting.')
		return None
	if store_command (_shell, ['a', 'o', _path]) is None :
		return None
	_shell.get_view () .get_scroll () .reset_touched ()
	_shell.notify ('save: saved.')
	return True


_go_arguments = None


def go_command (_shell, _arguments) :
	global _go_arguments
	if len (_arguments) == 0 :
		if _go_arguments is None :
			_shell.notify ('go: no previous go command; aborting.')
			return None
		_arguments = _go_arguments
	if len (_arguments) != 2 :
		_shell.notify ('go: wrong syntax: go l|s <argument>')
		return None
	_mode = _arguments[0]
	_argument = _arguments[1]
	if _mode not in ['l', 's'] :
		_shell.notify ('go: wrong mode (l|s); aborting.')
		return None
	_view = _shell.get_view ()
	_lines = _view.get_lines ()
	_cursor = _view.get_cursor ()
	if _lines == 0 :
		pass
	if _mode == 'l' :
		try :
			_line = int (_argument) - 1
		except :
			_shell.notify ('go: wrong line; aborting.')
			return None
		if _line > _lines :
			_line = _lines - 1
		_cursor.set_line (_line)
		_go_arguments = _arguments
		return True
	elif _mode == 's' :
		_line = _cursor.get_line () + 1
		if _line >= _lines :
			pass
		else :
			for _line in xrange (_line, _lines) :
				_column = _view.select_real_string (_line) .find (_argument)
				if _column >= 0 :
					break
			if _line < _lines :
				_cursor.set_line (_line)
				_cursor.set_column (_view.select_visual_column (_line, _column))
		_go_arguments = _arguments
		return True
	return None


def go_line_command (_shell, _arguments) :
	if len (_arguments) != 1 :
		_shell.notify ('go-line: wrong syntax: go-line <line>')
		return None
	_line = _arguments[0]
	if go_command (_shell, ['l', _line]) is None :
		return None
	return True


def go_string_command (_shell, _arguments) :
	if len (_arguments) != 1 :
		_shell.notify ('go-string: wrong syntax: go-string <string>')
		return None
	_string = _arguments[0]
	if go_command (_shell, ['s', _string]) is None :
		return None
	return True


_jump_line = None


def jump_command (_shell, _arguments) :
	global _jump_line
	if len (_arguments) == 0 :
		_arguments = ['j']
	if len (_arguments) != 1 :
		_shell.notify ('go: wrong syntax: jump s|j')
		return None
	_mode = _arguments[0]
	if _mode not in ['s', 'j'] :
		_shell.notify ('go: wrong mode (s|j); aborting.')
		return None
	_view = _shell.get_view ()
	_cursor = _view.get_cursor ()
	if _mode == 's' :
		_jump_line = _cursor.get_line ()
		return True
	elif _mode == 'j' :
		if _jump_line is None :
			_shell.notify ('jump: no previous jump set command; aborting.')
			return None
		_old_jump_line = _jump_line
		_jump_line = _cursor.get_line ()
		_cursor.set_line (_old_jump_line)
		return True
	return None


def jump_set_command (_shell, _arguments) :
	if len (_arguments) != 0 :
		_shell.notify ('jump-set: wrong syntax: jump-set')
		return None
	if jump_command (_shell, ['s']) is None :
		return None
	return True
