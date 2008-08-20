#!/usr/bin/python2.5


import curses
import codecs
import locale
import os
import os.path
import subprocess
import sys
import traceback


class Scroll :
	
	def __init__ (self) :
		self._lines = [u'']
	
	def is_empty (self) :
		return len (self._lines) == 0
	
	def get_length (self) :
		return len (self._lines)
	
	def select (self, _index) :
		return self._lines[_index]
	
	def update (self, _index, _string) :
		self._lines.add (unicode (_string))
	
	def append (self, _string) :
		if (len (self._lines) == 1) and (len (self._lines[0]) == 0) :
			self._lines[0] = _string
		else :
			self._lines.append (unicode (_string))
	
	def include_before (self, _index, _string) :
		self._lines.insert (_index, unicode (_string))
	
	def include_after (self, _index, _string) :
		self._lines.insert (_index + 1, unicode (_string))
	
	def exclude (self, _index) :
		del self._lines[_index]
		if len (self._lines) == 0 :
			self._lines = [u'']
	
	def empty (self) :
		self._lines = [u'']
	
	def split (self, _index, _column) :
		if (_column == 0) :
			self._lines.insert (_index, u'')
		else :
			_line = self._lines[_index]
			self._lines[_index] = _line[: _column]
			self._lines.insert (_index + 1, _line[_column :])
	
	def unsplit (self, _index) :
		_line_0 = self._lines[_index]
		_line_1 = self._lines[_index + 1]
		_line = _line_0 + _line_1
		del self._lines[_index + 1]
		self._lines[_index] = _line
	
	def insert (self, _index, _column, _string) :
		_line = self._lines[_index]
		if (_column == 0) :
			_line = unicode (_string) + _line
		elif (_column < len (_line)) :
			_line = _line[: _column] + unicode (_string) + _line[_column :]
		elif (_column == len (_line)) :
			_line = _line + unicode (_string)
		else :
			_line = _line + (' ' * (_column - len (_line))) + unicode (_string)
		self._lines[_index] = _line
	
	def delete (self, _index, _column, _length) :
		_line = self._lines[_index]
		if (_column > len (_line)) :
			pass
		elif (_column + _length) >= len (_line) :
			_line = _line[: _column]
		elif _column == 0 :
			_line = _line[_length :]
		else :
			_line = _line[: _column] + _line[_column + _length :]
		self._lines[_index] = _line
#


class Mark :
	
	def __init__ (self) :
		self._line = 0
		self._column = 0
	
	def get_line (self) :
		return self._line
	
	def get_column (self) :
		return self._column
	
	def set_line (self, _line) :
		self._line = _line
	
	def set_column (self, _column) :
		self._column = _column
	
	def increment_line (self, _increment) :
		self._line += _increment
	
	def increment_column (self, _increment) :
		self._column += _increment
#


class View :
	
	def __init__ (self) :
		self._cursor = Mark ()
		self._head = Mark ()
		self._tail = Mark ()
		self._max_lines = 1
		self._max_columns = 1
	
	def get_lines (self) :
		return 1
	
	def select_real_string (self, _line) :
		return ''
	
	def select_visual_string (self, _line, _head_column, _tail_column) :
		return []
	
	def select_real_column (self, _line, _visual_column) :
		return _visual_column
	
	def select_visual_column (self, _line, _real_column) :
		return _real_column
	
	def select_real_length (self, _line) :
		return 0
	
	def select_visual_length (self, _line) :
		return 0
	
	def select_tagged (self, _line) :
		return False
	
	def get_cursor (self) :
		return self._cursor
	
	def get_head (self) :
		return self._head
	
	def get_tail (self) :
		return self._tail
	
	def get_max_lines (self) :
		return self._max_lines
	
	def set_max_lines (self, _lines) :
		self._max_lines = _lines
	
	def get_max_columns (self) :
		return self._max_columns
	
	def set_max_columns (self, _columns) :
		self._max_columns = _columns
	
	def refresh (self) :
		
		_cursor_line = self._cursor._line
		_cursor_column = self._cursor._column
		_head_line = self._head._line
		_head_column = self._head._column
		_tail_line = self._tail._line
		_tail_column = self._tail._column
		_max_lines = self._max_lines
		_max_columns = self._max_columns
		_lines = self.get_lines ()
		
		if _cursor_line < 0 :
			_cursor_line = 0
		elif _cursor_line >= _lines :
			_cursor_line = _lines - 1
		if _cursor_column < 0 :
			_cursor_column = 0
		
		if _lines <= _max_lines :
			_head_line = 0
			_tail_line = _lines - 1
		else :
			if _cursor_line <= (_head_line + 5) :
				_head_line = _cursor_line - 5
				if _head_line < 0 :
					_head_line = 0
				_tail_line = _head_line + _max_lines - 1
			if _cursor_line >= (_tail_line - 5) :
				_tail_line = _cursor_line + 5
				if _tail_line >= _lines :
					_tail_line = _lines - 1
				_head_line = _tail_line - _max_lines + 1
		
		if _tail_column - _head_column < _max_columns :
			_tail_column = _head_column + _max_columns - 1
		if _cursor_column <= (_head_column + 10) :
			_head_column = _cursor_column - 10
			if _head_column < 0 :
				_head_column = 0
			_tail_column = _head_column + _max_columns - 1
		if _cursor_column >= (_tail_column - 10) :
			_tail_column = _cursor_column + 10
			_head_column = _tail_column - _max_columns + 1
		
		self._cursor._line = _cursor_line
		self._cursor._column = _cursor_column
		self._head._line = _head_line
		self._head._column = _head_column
		self._tail._line = _tail_line
		self._tail._column = _tail_column
#


class ScrollView (View) :
	
	def __init__ (self, _scroll) :
		View.__init__ (self)
		self._scroll = _scroll
		self._mark = Mark ()
		self._mark_enabled = False
		self._tab_columns = 4
	
	def get_scroll (self) :
		return self._scroll
	
	def get_lines (self) :
		return self._scroll.get_length ()
	
	def get_mark (self) :
		return self._mark
	
	def is_mark_enabled (self) :
		return self._mark_enabled
	
	def set_mark_enabled (self, _enabled) :
		self._mark_enabled = _enabled
	
	def select_real_string (self, _line) :
		return self._scroll.select (_line)
	
	def select_visual_string (self, _line, _head_column, _tail_column) :
		return self.compute_visual_string (self._scroll.select (_line), _head_column, _tail_column)
	
	def select_real_column (self, _line, _visual_column) :
		return self.compute_real_column (self._scroll.select (_line), _visual_column)
	
	def select_visual_column (self, _line, _real_column) :
		return self.compute_visual_column (self._scroll.select (_line), _real_column)
	
	def select_real_length (self, _line) :
		return len (self._scroll.select (_line))
	
	def select_visual_length (self, _line) :
		return self.compute_visual_length (self._scroll.select (_line))
	
	def select_tagged (self, _line) :
		_cursor_line = self._cursor.get_line ()
		_mark_line = self._mark.get_line ()
		return self._mark_enabled and ((_cursor_line <= _line <= _mark_line) or (_mark_line <= _line <= _cursor_line))
	
	def refresh (self) :
		
		View.refresh (self)
		
		_mark_line = self._mark._line
		_mark_column = self._mark._column
		_lines = self.get_lines ()
		
		if _mark_line < 0 :
			_mark_line = 0
		elif _mark_line >= _lines :
			_mark_line = _lines - 1
		if _mark_column < 0 :
			_mark_column = 0
		
		self._mark._line = _mark_line
		self._mark._column = _mark_column
	
	def compute_real_column (self, _string, _column) :
		_tab_columns = self._tab_columns
		_index = 0
		_length = 0
		for _character in _string :
			_code = ord (_character)
			if _code == 9 :
				_length = ((_length / _tab_columns) + 1) * _tab_columns
			else :
				_length += 1
			if _length > _column :
				break
			_index += 1
		if _length < _column :
			_index += _column - _length
		return _index
	
	def compute_visual_column (self, _string, _column) :
		_tab_columns = self._tab_columns
		_index = 0
		_length = 0
		for _character in _string :
			_code = ord (_character)
			if _index == _column :
				break
			if _code == 9 :
				_length = ((_length / _tab_columns) + 1) * _tab_columns
			else :
				_length += 1
			_index += 1
		if _index < _column :
			_length += _column - _index
		return _length
	
	def compute_visual_length (self, _string) :
		_tab_columns = self._tab_columns
		_length = 0
		for _character in _string :
			_code = ord (_character)
			if _code == 9 :
				_length = ((_length / _tab_columns) + 1) * _tab_columns
			else :
				_length += 1
		return _length

	def compute_visual_string (self, _string, _head_column, _tail_column) :
		_tab_columns = self._tab_columns
		_buffer = []
		_column = 0
		_code = 0
		_h_code = ord ('-')
		_g_code = ord ('>')
		_e_code = ord ('!')
		_last_mode = None
		_last_code = None
		for _character in _string :
			_code = ord (_character)
			if _code == 9 :
				_delta = (((_column / _tab_columns) + 1) * _tab_columns) - _column
				if ((_column + _delta) > _head_column) and (_column <= _tail_column) :
					if _last_mode != -2 :
						_buffer.append (-2)
						_last_mode = -2
					if (_column >= _head_column) and ((_column + _delta) <= _tail_column) :
						_buffer.extend ([_h_code] * (_delta - 1))
					else :
						if _column < _head_column :
							_buffer.extend ([_h_code] * (_column + _delta - _head_column - 1))
						if _column + _delta > _tail_column :
							_buffer.extend ([_h_code] * (_tail_column - _column))
					_buffer.append (_g_code)
				_column += _delta
			else :
				if (_column >= _head_column) and (_column <= _tail_column) :
					if _last_mode != -1 :
						_buffer.append (-1)
						_last_mode = -1
					_buffer.append (_code)
				_column += 1
			_last_code = _code
			if _column >= _tail_column :
				break
		if _column <= _tail_column and _last_code == 32 :
			if _last_mode != -3 :
				_buffer.append (-3)
				_last_mode = -3
			_buffer.append (_e_code)
		return _buffer
#


class Shell :
	
	def __init__ (self, _view, _handler) :
		self._view = _view
		self._handler = _handler
		self._messages = []
		self._messages_touched = False
		self._max_message_lines = 10
		self._inputs = []
		self._max_input_lines = 3
	
	def get_view (self) :
		return self._view
	
	def get_handler (self) :
		return self._key_handler
	
	def open (self) :
		
		locale.setlocale (locale.LC_ALL,'')
		
		self._window = curses.initscr ()
		
		curses.start_color ()
		curses.use_default_colors ()
		curses.init_pair (1, curses.COLOR_WHITE, -1)
		curses.init_pair (2, curses.COLOR_BLUE, -1)
		curses.init_pair (3, curses.COLOR_RED, -1)
		curses.init_pair (4, curses.COLOR_MAGENTA, -1)
		curses.init_pair (5, curses.COLOR_GREEN, -1)
		self._color_text = curses.color_pair (1)
		self._color_markup = curses.color_pair (2)
		self._color_error = curses.color_pair (3)
		self._color_message = curses.color_pair (4)
		self._color_input = curses.color_pair (5)
		
		self.show ()
	
	def close (self) :
		
		self.hide ()
		
		del self._window
		del self._window_lines
		del self._window_columns
		del self._color_text
		del self._color_markup
		del self._color_message
		del self._color_input
	
	def show (self) :
		self._window = curses.initscr ()
		curses.raw ()
		#curses.cbreak ()
		curses.noecho ()
		curses.nonl ()
		self._window.keypad (1)
		self._window.leaveok (0)
		(self._window_lines, self._window_columns) = self._window.getmaxyx ()
		self._view.set_max_lines (self._window_lines)
		self._view.set_max_columns (self._window_columns - 1)
		self._view.refresh ()
	
	def hide (self) :
		self._window.keypad (0)
		self._window.leaveok (1)
		curses.nl ()
		curses.echo ()
		#curses.nocbreak ()
		curses.noraw ()
		curses.endwin ()
	
	def scan (self) :
		return self._window.getch ()
	
	def flush (self) :
		curses.flushinp ()
	
	def alert (self) :
		curses.beep ()
	
	def notify (self, _format, *_arguments) :
		self._messages.insert (0, _format % _arguments)
		del self._messages[self._max_message_lines :]
		self._messages_touched = True
	
	def loop (self) :
		try :
			self._loop = True
			self.refresh ()
			while self._loop :
				self._handler.handle_key (self, self.scan ())
				self.refresh ()
		except Exception, _error :
			return (_error, traceback.format_exc ())
		except :
			return (None, '<<unknown system error>>')
		return None
	
	def loop_stop (self) :
		self._loop = False
	
	def input (self, _format, *_arguments) :
		
		_window = self._window
		_line = self._window_lines - self._max_input_lines
		
		_window.move (_line, 0)
		_window.clrtobot ()
		_window.attrset (self._color_input)
		_window.addstr ('[??] ')
		_window.addstr ((_format % _arguments) .encode ('utf-8'))
		_window.move (_line + 1, 0)
		_window.addstr ('[>>] ')
		_window.refresh ()
		
		_buffer = []
		_inputs = self._inputs
		_input = len (_inputs) - 1
		while True :
			_string = u''.join (_buffer)
			_window.move (_line + 1, 5)
			_window.clrtobot ()
			_window.addstr (_string .encode ('utf-8'))
			_window.refresh ()
			_code = _window.getch ()
			if (_code >= 32) and (_code < 127) :
				_buffer.append (chr (_code))
			elif (_code >= 194) and (_code < 224) :
				_buffer.append ((chr (_code) + chr (_window.scan ())) .decode ('utf-8'))
			elif (_code == curses.KEY_BACKSPACE) or (_code == 8) :
				if len (_buffer) > 0 :
					_buffer.pop ()
				else :
					curses.beep ()
			elif (_code == curses.KEY_ENTER) or (_code == 10) or (_code == 13) :
				if len (_buffer) > 0 :
					_inputs.append (_string)
				else :
					_string = None
				break
			elif _code == 11 : # Ctrl+K
				if len (_buffer) == 0 :
					break
				else :
					_buffer = []
			elif (_code == curses.KEY_UP) :
				if _input == -1 :
					curses.beep ()
					continue
				_input -= 1
				if _input < 0 :
					_input = len (_inputs) -1
				_buffer = []
				_buffer.extend (_inputs[_input])
			elif (_code == curses.KEY_DOWN) :
				if _input == -1 :
					curses.beep ()
					continue
				_input += 1
				if _input >= len (_inputs) :
					_input = 0
				_buffer = []
				_buffer.extend (_inputs[_input])
			else :
				curses.beep ()
		
		return _string
	
	def refresh (self) :
		
		_view = self._view
		_view.refresh ()
		
		_cursor = _view.get_cursor ()
		_head = _view.get_head ()
		_tail = _view.get_tail ()
		
		_lines = _view.get_lines ()
		_cursor_line = _cursor.get_line ()
		_cursor_column = _cursor.get_column ()
		_head_line = _head.get_line ()
		_head_column = _head.get_column ()
		_tail_line = _tail.get_line ()
		_tail_column = _tail.get_column ()
		_max_lines = self._window_lines
		_max_columns = self._window_columns - 1
		
		_messages = self._messages
		_messages_touched = self._messages_touched
		self._messages_touched = False
		
		_window = self._window
		_color_text = self._color_text
		_color_markup = self._color_markup
		_color_error = self._color_error
		_color_message = self._color_message
		
		_window.erase ()
		
		for i in xrange (0, _max_lines) :
			_window.move (i, 0)
			_line = _head_line + i
			if _line < _lines :
				_window.attrset (_color_markup)
				if _view.select_tagged (_line) :
					_window.addstr ('#')
				else :
					_window.addstr (' ')
				_buffer = _view.select_visual_string (_line, _head_column, _tail_column)
				for _code in _buffer :
					if _code >= 0 :
						_window.addstr (unichr (_code) .encode ('utf-8'))
					elif _code == -1 :
						_window.attrset (_color_text)
					elif _code == -2 :
						_window.attrset (_color_markup)
					elif _code == -3 :
						_window.attrset (_color_error)
					else :
						_window.addstr ('?')
			else :
				_window.attrset (_color_markup)
				_window.addstr ('-----')
				break
		
		_window.move (_cursor_line - _head_line, _cursor_column - _head_column + 1)
		
		if _messages_touched :
			_index = 0
			_window.attrset (_color_message)
			for _message in _messages :
				_window.move (_max_lines - _index - 1, 0)
				_window.clrtoeol ()
				_window.addstr ('[..] ')
				_window.addstr (_message.encode ('utf-8'))
				_index += 1
			_window.move (_max_lines - 1, _max_columns - 1)
		
		_window.refresh ()
#


class Handler :
	
	def __init__ (self) :
		pass
	
	def handle_key (self, _shell, _code) :
		
		if _code < 0 :
			self.handle_key_unknown (_shell, 'Code:%d' % (_code))
		
		elif (_code >= 32) and (_code < 127) :
			self.handle_key_character (_shell, chr (_code))
		elif (_code >= 194) and (_code < 224) :
			_char = (chr (_code) + chr (_shell.scan ())) .decode ('utf-8')
			self.handle_key_character (_shell, _char)
		
		elif _code == 8 : # Backspace
			self.handle_key_backspace (_shell)
		elif _code == 9 : # Tab
			self.handle_key_tab (_shell)
		elif _code == 10 : # Enter
			self.handle_key_enter (_shell)
		elif _code == 13 : # Enter
			self.handle_key_enter (_shell)
		elif _code == 27 : # Escape
			self.handle_key_escape (_shell)
		elif _code == 127 : # Delete
			self.handle_key_delete (_shell)
		
		elif (_code >= 0) and (_code < 32) :
			self.handle_key_control (_shell, _code)
		
		elif _code == curses.KEY_UP :
			self.handle_key_up (_shell)
		elif _code == curses.KEY_DOWN :
			self.handle_key_down (_shell)
		elif _code == curses.KEY_LEFT :
			self.handle_key_left (_shell)
		elif _code == curses.KEY_RIGHT :
			self.handle_key_right (_shell)
		
		elif _code == curses.KEY_HOME :
			self.handle_key_home (_shell)
		elif _code == curses.KEY_END :
			self.handle_key_end (_shell)
		
		elif _code == curses.KEY_PPAGE :
			self.handle_key_page_up (_shell)
		elif _code == curses.KEY_NPAGE :
			self.handle_key_page_down (_shell)
		
		elif _code == curses.KEY_IC :
			self.handle_key_insert (_shell)
		elif _code == curses.KEY_DC :
			self.handle_key_delete (_shell)
		
		elif _code == curses.KEY_BACKSPACE :
			self.handle_key_backspace (_shell)
		elif _code == curses.KEY_ENTER :
			self.handle_key_enter (_shell)
		
		elif (_code >= curses.KEY_F0) and (_code <= curses.KEY_F63) :
			self.handle_key_function (_shell, _code - curses.KEY_F0)
		
		else :
			self.handle_key_unknown (_shell, 'Code:%d' % (_code))
		
		return True
	
	def handle_key_backspace (self, _shell) :
		self.handle_key_unknown (_shell, 'Backspace')
	
	def handle_key_tab (self, _shell) :
		self.handle_key_unknown (_shell, 'Tab')
	
	def handle_key_enter (self, _shell) :
		self.handle_key_unknown (_shell, 'Enter')
	
	def handle_key_escape (self, _shell) :
		self.handle_key_unknown (_shell, 'Escape')
	
	def handle_key_delete (self, _shell) :
		self.handle_key_unknown (_shell, 'Delete')
	
	def handle_key_control (self, _shell, _code) :
		self.handle_key_unknown (_shell, 'Ctrl+%s' % (chr (64 + _code)))
	
	def handle_key_character (self, _shell, _character) :
		self.handle_key_unknown (_shell, _character)
	
	def handle_key_up (self, _shell) :
		self.handle_key_unknown (_shell, 'Up')
	
	def handle_key_down (self, _shell) :
		self.handle_key_unknown (_shell, 'Down')
	
	def handle_key_left (self, _shell) :
		self.handle_key_unknown (_shell, 'Left')
	
	def handle_key_right (self, _shell) :
		self.handle_key_unknown (_shell, 'Right')
	
	def handle_key_home (self, _shell) :
		self.handle_key_unknown (_shell, 'Home')
	
	def handle_key_end (self, _shell) :
		self.handle_key_unknown (_shell, 'End')
	
	def handle_key_page_up (self, _shell) :
		self.handle_key_unknown (_shell, 'Page up')
	
	def handle_key_page_down (self, _shell) :
		self.handle_key_unknown (_shell, 'Page down')
	
	def handle_key_insert (self, _shell) :
		self.handle_key_unknown (_shell, 'Insert')
	
	def handle_key_function (self, _shell, _code) :
		self.handle_key_unknown (_shell, 'F%d' % (_code))
	
	def handle_key_unknown (self, _shell, _key) :
		_shell.notify ('Unhandled key [%s]; ignoring.', _key)
#


class BasicHandler (Handler) :
	
	def __init__ (self) :
		Handler.__init__ (self)
		self._commands = dict ()
		self._controls = dict ()
	
	def handle_key_up (self, _shell) :
		_shell.get_view () .get_cursor () .increment_line (-1)
	
	def handle_key_down (self, _shell) :
		_shell.get_view () .get_cursor () .increment_line (1)
	
	def handle_key_left (self, _shell) :
		_shell.get_view () .get_cursor () .increment_column (-1)
	
	def handle_key_right (self, _shell) :
		_shell.get_view () .get_cursor () .increment_column (1)
	
	def handle_key_home (self, _shell) :
		_shell.get_view () .get_cursor () .set_column (0)
	
	def handle_key_end (self, _shell) :
		_view = _shell.get_view ()
		_cursor = _view.get_cursor ()
		_cursor.set_column (_view.select_visual_length (_cursor.get_line ()))
	
	def handle_key_page_up (self, _shell) :
		_view = _shell.get_view ()
		_view.get_cursor () .increment_line (- _view.get_max_lines ())
	
	def handle_key_page_down (self, _shell) :
		_view = _shell.get_view ()
		_view.get_cursor () .increment_line (_view.get_max_lines ())
	
	def handle_key_control (self, _shell, _code) :
		if _code not in self._controls :
			self.handle_key_unknown (_shell, 'Ctrl+%s' % (chr (64 + _code)))
			return
		_handler = self._controls[_code]
		try :
			_handler (_shell, [])
		except Exception, _error :
			_shell.notify ('Unhandled exception [%s]; ignoring.', str (_error))
		except :
			_shell.notify ('Unhandled system exception; ignoring.')
	
	def handle_command (self, _shell, _arguments) :
		_command = _shell.input ('Command?')
		if _command is None :
			return
		_parts = _command.split ()
		if len (_parts) == 0 :
			return
		if _parts[0] not in self._commands :
			_shell.notify ('Unhandled command [%s]; ignoring.', _parts[0])
			return
		_handler = self._commands[_parts[0]]
		try :
			_handler (_shell, _parts[1 :])
		except Exception, _error :
			_shell.notify ('Unhandled exception [%s]; ignoring.', str (_error))
		except :
			_shell.notify ('Unhandled system exception; ignoring.')
	
	def register_command (self, _command, _handler) :
		self._commands[_command] = _handler
	
	def unregister_command (self, _command) :
		del self._commands[_command]
	
	def register_control (self, _control, _handler) :
		self._controls[ord (_control) - 64] = _handler
	
	def unregister_control (self, _control) :
		del self._controls[ord (_control) - 64]
#


class ScrollHandler (BasicHandler) :
	
	def __init__ (self) :
		BasicHandler.__init__ (self)
	
	def handle_key_backspace (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_length = _view.select_visual_length (_line)
		if _visual_column > _length :
			_cursor.set_column (_length)
		elif _visual_column > 0 :
			_real_column = _view.select_real_column (_line, _visual_column - 1)
			_scroll.delete (_line, _real_column, 1)
			_cursor.set_column (_view.select_visual_column (_line, _real_column))
		elif _line > 0 :
			_length = _view.select_visual_length (_line - 1)
			_scroll.unsplit (_line - 1)
			_cursor.increment_line (-1)
			_cursor.set_column (_length)
		else :
			_shell.alert ()
	
	def handle_key_tab (self, _shell) :
		self._insert_character (_shell, '\t')
	
	def handle_key_enter (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_scroll.split (_line, _view.select_real_column (_line, _cursor.get_column ()))
		_cursor.increment_line (1)
		_cursor.set_column (0)
	
	def handle_key_delete (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_length = _view.select_visual_length (_line)
		if _visual_column > _length :
			_cursor.set_column (_length)
		elif _visual_column < _length :
			_real_column = _view.select_real_column (_line, _visual_column)
			_scroll.delete (_line, _real_column, 1)
			_cursor.set_column (_view.select_visual_column (_line, _real_column))
		elif _line < (_scroll.get_length () - 1) :
			_scroll.unsplit (_line)
			_cursor.set_column (_length)
		else :
			_shell.alert ()
	
	def handle_key_character (self, _shell, _character) :
		self._insert_character (_shell, _character)
	
	def _insert_character (self, _shell, _character) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_real_column = _view.select_real_column (_line, _visual_column)
		_scroll.insert (_line, _real_column, _character)
		_cursor.set_column (_view.select_visual_column (_line, _real_column + 1))
#


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
		for _line in _yank_buffer :
			_scroll.include_before (_cursor_line, _line)
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
	_yank_buffer = []
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
			for _line in xrange (_first_line, _last_line + 1) :
				_yank_buffer.append (_scroll.select (_line))
			_yank_buffer.reverse ()
		_view.set_mark_enabled (False)
	else :
		_yank_buffer.append (_scroll.select (_cursor_line))


def delete_lines_command (_shell, _arguments) :
	global _yank_buffer
	if len (_arguments) != 0 :
		_shell.notify ('delete-lines: wrong syntax: delete-lines')
		return
	_yank_buffer = []
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	_cursor = _view.get_cursor ()
	_cursor_line = _cursor.get_line ()
	if _view.is_mark_enabled () :
		_mark_line = _view.get_mark () .get_line ()
		_first_line = min (_mark_line, _cursor_line)
		_last_line = max (_mark_line, _cursor_line)
		for _line in xrange (_first_line, _last_line + 1) :
			_yank_buffer.append (_scroll.select (_first_line))
			_scroll.exclude (_first_line)
		_view.set_mark_enabled (False)
		_cursor.set_line (_first_line)
	else :
		_yank_buffer.append (_scroll.select (_cursor_line))
		_scroll.exclude (_cursor_line)
	_yank_buffer.reverse ()


def load_command (_shell, _arguments) :
	if len (_arguments) != 2 :
		_shell.notify ('load: wrong syntax: load r|i|a <path>')
		return
	_type = _arguments[0]
	_path = _arguments[1]
	if _type not in ['r', 'i', 'a'] :
		_shell.notify ('load: wrong type; aborting.')
		return
	if not os.path.isfile (_path) :
		_shell.notify ('load: wrong path; aborting.')
		return
	_stream = codecs.open (_path, 'r', 'utf-8')
	_lines = _stream.readlines ()
	_stream.close ()
	_handle_file_lines (_shell, _type, _lines)


def sys_command (_shell, _arguments) :
	if len (_arguments) < 2 :
		_shell.notify ('sys: wrong syntax: sys r|i|a <command> <argument> ...')
		return
	_type = _arguments[0]
	if _type not in ['r', 'i', 'a'] :
		_shell.notify ('sys: wrong type; aborting.')
		return
	_system_arguments = _arguments[1 :]
	_shell.hide ()
	try :
		_process = subprocess.Popen (
				_system_arguments, shell = False, env = None,
				stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 1, close_fds = True, universal_newlines = True)
	except :
		_shell.show ()
		_shell.notify ('sys: wrong command; aborting.')
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
		_shell.notify ('sys: command failed; aborting.')
		return
	_shell.show ()
	if _error != 0 :
		_shell.notify ('sys: command failed; ignoring.')
	if len (_error_lines) != 0 :
		for _line in _error_lines :
			_line = _line.rstrip ('\r\n')
			_shell.notify ('sys: %s', _line)
	_handle_file_lines (_shell, _type, _lines)


def _handle_file_lines (_shell, _type, _lines) :
	_view = _shell.get_view ()
	_scroll = _view.get_scroll ()
	if _type == 'r' :
		_scroll.empty ()
		_insert_line = 0
	elif _type == 'i' :
		_insert_line = _view.get_cursor () .get_line ()
	elif _type == 'a' :
		_insert_line = _scroll.get_length () - 1
	else :
		_insert_line = _scroll.get_length () - 1
	_lines.reverse ()
	for _line in _lines :
		_line = _line.rstrip ('\r\n')
		_scroll.include_before (_insert_line, _line)


def sce (_arguments) :
	_scroll = Scroll ()
	_view = ScrollView (_scroll)
	_handler = ScrollHandler ()
	#_handler.register_control ('X', exit_command)
	_handler.register_control ('@', mark_command)
	_handler.register_control ('R', _handler.handle_command)
	_handler.register_control ('Y', yank_lines_command)
	_handler.register_control ('D', copy_lines_command)
	_handler.register_control ('K', delete_lines_command)
	_handler.register_command ('clear', clear_command)
	_handler.register_command ('exit', exit_command)
	_handler.register_command ('load', load_command)
	_handler.register_command ('sys', sys_command)
	_shell = Shell (_view, _handler)
	_shell.open ()
	for _argument in sys.argv[1 :] :
		load_command (_shell, ['a', _argument])
	_error = _shell.loop ()
	_shell.close ()
	if _error is not None :
		print _error[0]
		print _error[1]
	print


sce (sys.argv[1 :])
