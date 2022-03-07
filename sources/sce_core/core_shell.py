
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *

__all__ = [
		"Shell",
	]


class Shell (object) :
	
	def __init__ (self) :
		self._view = None
		self._handler = None
		self._messages = []
		self._messages_touched = False
		self._max_message_lines = 10
		self._max_message_timeout = 3
		self._inputs = []
		self._backspace_code = 127
		self._delete_code = 330
		self._opened = False
		self._terminal = None
	
	def get_view (self) :
		return self._view
	
	def set_view (self, _view) :
		self._view = _view
	
	def get_handler (self) :
		return self._key_handler
	
	def set_handler (self, _handler) :
		self._handler = _handler
	
	def set_terminal (self, _terminal) :
		self._terminal = _terminal
	
	def open (self) :
		
		_terminal_descriptor = self._terminal.fileno ()
		if not os.isatty (_terminal_descriptor) :
			return False
		
		# FIXME: These should not be needed, but it seems `setupterm` doesn't do all its job...
		if _terminal_descriptor != 0 :
			os.dup2 (_terminal_descriptor, 0)
		if _terminal_descriptor != 1 :
			os.dup2 (_terminal_descriptor, 1)
		if _terminal_descriptor != 2 :
			os.dup2 (_terminal_descriptor, 2)
		
		for _locale in ["C.UTF-8", "en_US.UTF-8", "C"] :
			try :
				os.environ["LANG"] = _locale
				os.environ["LC_ALL"] = _locale
				locale.setlocale (locale.LC_ALL, _locale)
				break
			except :
				del os.environ["LANG"]
				del os.environ["LC_ALL"]
				pass
		
		curses.setupterm (os.environ["TERM"], _terminal_descriptor)
		
		self._curses_open ()
		
		self._opened = True
		
		return None
	
	def close (self) :
		
		self._curses_close ()
		
		self._opened = False
		
		return None
	
	def _curses_open (self) :
		
		self._window = curses.initscr ()
		
		curses.savetty ()
		
		curses.start_color ()
		curses.use_default_colors ()
		curses.init_pair (1, curses.COLOR_WHITE, -1)
		curses.init_pair (2, curses.COLOR_BLUE, -1)
		curses.init_pair (3, curses.COLOR_RED, -1)
		curses.init_pair (4, curses.COLOR_MAGENTA, -1)
		curses.init_pair (5, curses.COLOR_GREEN, -1)
		curses.init_pair (6, curses.COLOR_YELLOW, -1)
		curses.init_pair (7, curses.COLOR_RED, -1)
		self._color_text = curses.color_pair (1) | curses.A_NORMAL
		self._color_markup = curses.color_pair (2) | curses.A_NORMAL
		self._color_error = curses.color_pair (3) | curses.A_BOLD
		self._color_message = curses.color_pair (4) | curses.A_NORMAL
		self._color_input = curses.color_pair (5) | curses.A_NORMAL
		self._color_highlight_1 = curses.color_pair (6) | curses.A_BOLD
		self._color_highlight_2 = curses.color_pair (7) | curses.A_BOLD
		
		curses.noecho ()
		curses.nonl ()
		curses.raw ()
		curses.meta (1)
		
		self._window.leaveok (0)
		self._window.idcok (0)
		self._window.idlok (0)
		self._window.immedok (0)
		self._window.keypad (1)
		self._window.notimeout (0)
		self._window.scrollok (0)
		
		self._window.erase ()
		curses.doupdate ()
		
		curses.flushinp ()
		
		return None
	
	def _curses_close (self) :
		
		self._window.erase ()
		curses.doupdate ()
		
		del self._window
		del self._color_text
		del self._color_markup
		del self._color_message
		del self._color_input
		
		curses.echo ()
		curses.nl ()
		curses.noraw ()
		
		curses.flushinp ()
		
		curses.resetty ()
		
		curses.endwin ()
		
		return None
	
	def scan (self) :
		_window = self._window
		_code = _window.getch ()
		if _code < 0 :
			pass
		elif _code == 27 :
			_window.nodelay (True)
			_codes = []
			while True :
				_code = _window.getch ()
				if _code == -1 :
					break
				_codes.append ("%d" % _code)
			_window.nodelay (False)
			if len (_codes) > 0 :
				_code = ":".join (_codes)
				_code = "\33:" + _code
			else :
				_code = 27
		elif (_code >= 0) and (_code < 32) :
			pass
		elif (_code >= 32) and (_code < 127) :
			_code = bytechr_ (_code) .decode ("utf-8")
		elif _code == 127 :
			pass
		elif (_code >= 128) and (_code < 192) :
			_code = None
		elif (_code >= 192) and (_code < 194) :
			_code = None
		elif (_code >= 194) and (_code < 224) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code = (bytechr_ (_code_1) + bytechr_ (_code_2)) .decode ("utf-8")
		elif (_code >= 224) and (_code < 240) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code_3 = _window.getch ()
			_code = (bytechr_ (_code_1) + bytechr_ (_code_2) + bytechr_ (_code_3)) .decode ("utf-8")
		elif (_code >= 240) and (_code < 245) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code_3 = _window.getch ()
			_code_4 = _window.getch ()
			_code = (bytechr_ (_code_1) + bytechr_ (_code_2) + bytechr_ (_code_3) + bytechr_ (_code_4)) .decode ("utf-8")
		elif (_code >= 245) and (_code < 248) :
			_code = None
		elif (_code >= 248) and (_code < 252) :
			_code = None
		elif (_code >= 252) and (_code < 254) :
			_code = None
		elif (_code >= 254) and (_code < 256) :
			_code = None
		elif (_code >= 256) :
			pass
		else :
			_code = None
		return _code
	
	def alert (self) :
		curses.beep ()
	
	def notify (self, _format, *_arguments) :
		return self.notify_0 (_format, _arguments, False)
	
	def notify_no_tty (self, _format, *_arguments) :
		return self.notify_0 (_format, _arguments, True)
	
	def notify_0 (self, _format, _arguments, _tty_skip) :
		_message = _format % _arguments
		_message_timestamp = time.time ()
		self._messages.insert (0, (_message_timestamp, (time.strftime ("[%H:%M:%S]", time.gmtime (_message_timestamp))), _message))
		del self._messages[self._max_message_lines :]
		self._messages_touched = _message_timestamp
		if not self._opened and not _tty_skip :
			_message = _format % _arguments
			self._terminal.write ("[..]  " + _message + "\n")
	
	def loop (self) :
		try :
			self._loop = True
			self.refresh ()
			while self._loop :
				self._handler.handle_key (self, self.scan ())
				self.refresh ()
		except :
			_error = sys.exc_info ()
			_traceback = traceback.format_exception (_error[0], _error[1], _error[2])
			_error = (_error[1], _traceback)
			return _error
		return None
	
	def loop_stop (self) :
		self._loop = False
	
	def input (self, _format, *_arguments) :
		_window = self._window
		(_window_lines, _window_columns) = _window.getmaxyx ()
		_request_line = _window_lines - 2
		_request_max_length = _window_columns - 5 - 1
		_response_line = _window_lines - 1
		_response_max_length = _window_columns - 5 - 1
		_request = _format % _arguments
		if len (_request) > _request_max_length :
			_request = _request[:_request_max_length - 6] + " [...]"
		_window.attrset (self._color_input)
		_window.move (_request_line, 0)
		_window.clrtoeol ()
		_window.insstr (("[??] " + _request) .encode ("utf-8"))
		_buffer = []
		_buffer_position = 0
		_inputs = self._inputs
		_inputs_count = len (_inputs)
		_input = _inputs_count
		while True :
			_buffer_string = "".join (_buffer)
			_response = _buffer_string
			_response_length = len (_response)
			_response_position = _buffer_position
			if _response_length > _response_max_length :
				_response_drop = _response_length - _response_max_length + 6
				if _response_position >= (_response_length - (_response_max_length // 2)) :
					_response = "[...] " + _response[_response_drop : _response_length]
					_response_position = _response_position + 6 - _response_drop
				elif _response_position < (_response_max_length - (_response_max_length // 2) - 1) :
					_response = _response[0 : _response_length - _response_drop] + " [...]"
				else :
					_response_trim_left = (_response_max_length - 6) // 2
					_response_trim_right = (_response_max_length - 6) // 2 + (_response_max_length - 6) % 2
					if (_response_position - _response_trim_left) < 0 :
						_response_trim_left -= _response_position - _response_trim_left
						_response_trim_right += _response_position - _response_trim_left
					if (_response_position + _response_trim_right) > _response_length :
						_response_trim_left -= _response_length - (_response_position + _response_trim_right)
						_response_trim_right += _response_length - (_response_position + _response_trim_right)
					if (_response_trim_left + _response_trim_right + 6) != _response_max_length :
						raise Exception ("[49d65f2a]")
					_response = "<] " + _response[(_response_position - _response_trim_left) : (_response_position + _response_trim_right)] + " [>"
					_response_position = 3 + _response_trim_left
			_window.move (_response_line, 0)
			_window.clrtoeol ()
			_window.insstr (("[>>] " + _response) .encode ("utf-8"))
			_window.move (_response_line, 5 + _response_position)
			_window.noutrefresh ()
			curses.doupdate ()
			_code = self.scan ()
			if _code is None :
				curses.beep ()
			elif isinstance (_code, basestring_) :
				if len (_code) > 1 and _code[0] == "\33" :
					curses.beep ()
				else :
					_buffer.insert (_buffer_position, _code)
					_buffer_position += 1
			elif not isinstance (_code, int) :
				curses.beep ()
			elif (_code == curses.KEY_BACKSPACE) or (_code == self._backspace_code) or (_code == 8) :
				if _buffer_position > 0 :
					_buffer.pop (_buffer_position - 1)
					_buffer_position -= 1
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_DC) or (_code == self._delete_code) :
				if _buffer_position < len (_buffer) :
					_buffer.pop (_buffer_position)
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_LEFT) :
				if _buffer_position > 0 :
					_buffer_position -= 1
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_RIGHT) :
				if _buffer_position < len (_buffer) :
					_buffer_position += 1
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_HOME) :
				if _buffer_position > 0 :
					_buffer_position = 0
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_END) :
				if _buffer_position < len (_buffer) :
					_buffer_position = len (_buffer)
				else :
					pass #! curses.beep ()
			elif (_code == curses.KEY_ENTER) or (_code == 10) or (_code == 13) :
				if len (_buffer) > 0 :
					_inputs.append (_buffer_string)
				else :
					_buffer_string = None
				break
			elif (_code == 27) or (_code == 24) : # Escape or Ctrl+X
				if len (_buffer) == 0 :
					break
				else :
					_buffer = []
					_buffer_position = 0
			elif (_code == curses.KEY_UP) or (_code == curses.KEY_DOWN) :
				if _inputs_count == 0 :
					curses.beep ()
					continue
				if _code == curses.KEY_UP :
					_input -= 1
				elif _code == curses.KEY_DOWN :
					_input += 1
				_buffer = []
				_buffer_position = 0
				if (_input == -1) or (_input == _inputs_count) :
					curses.beep ()
					continue
				if _input < 0 :
					_input = _inputs_count - 1
				if _input > _inputs_count :
					_input = 0
				_buffer = list (_inputs[_input])
				_buffer_position = len (_buffer)
			else :
				curses.beep ()
		return _buffer_string
	
	def refresh (self) :
		
		_window = self._window
		(_window_lines, _window_columns) = self._window.getmaxyx ()
		
		_color_text = self._color_text
		_color_markup = self._color_markup
		_color_error = self._color_error
		_color_message = self._color_message
		_color_highlight_1 = self._color_highlight_1
		_color_highlight_2 = self._color_highlight_2
		
		_window.erase ()
		
		_max_lines = _window_lines
		_max_columns = _window_columns - 1
		
		if self._messages_touched is not False :
			_time_now = time.time ()
			while True :
				if len (self._messages) == 0 :
					self._messages_touched = False
					break
				if (_time_now - self._messages[-1][0]) >= self._max_message_timeout :
					self._messages.pop (-1)
					continue
				break
		if self._messages_touched is not False :
			_max_lines -= len (self._messages)
		
		_view = self._view
		_view.set_max_lines (_max_lines)
		_view.set_max_columns (_max_columns)
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
		
		_messages = self._messages
		
		for i in xrange_ (0, _max_lines) :
			_window.move (i, 0)
			_line = _head_line + i
			_column = 0
			if _line >= 0 and _line < _lines :
				_window.attrset (_color_markup)
				if _view.select_is_tagged (_line) :
					_window.insstr (i, _column, "|")
					_column += 1
				else :
					_window.insstr (i, _column, " ")
					_column += 1
				_buffer = _view.select_visual_string (_line, _head_column, _tail_column)
				for _code in _buffer :
					if isinstance (_code, basestring_) :
						_window.insstr (i, _column, _code.encode ("utf-8"))
						_column += len (_code)
					elif _code == -1 :
						_window.attrset (_color_text)
					elif _code == -2 :
						_window.attrset (_color_markup)
					elif _code == -3 :
						_window.attrset (_color_error)
					elif _code == -4 :
						_window.attrset (_color_highlight_1)
					elif _code == -5 :
						_window.attrset (_color_highlight_2)
					else :
						_window.insstr (i, _column, "?")
						_column += 1
			else :
				_window.attrset (_color_markup)
				if True :
					if _line == 0 :
						_window.insstr (i, 0, "#")
					elif (_line == -1 or _line == _lines) and _lines > 0 :
						_window.insstr (i, 0, "~~~~~~~~")
					else :
						_window.insstr (i, 0, "~")
				else :
					if _line == _head_line and _line == _tail_line :
						_window.insstr (i, 0, "><")
					elif _line == 0 :
						_window.insstr (i, 0, "#")
					elif _line == _head_line :
						_window.insstr (i, 0, ">>")
					elif _line == _tail_line :
						_window.insstr (i, 0, "<<")
					elif (_line == -1 or _line == _lines) and _lines > 0 :
						_window.insstr (i, 0, "~~~~~~~~")
					elif _line < 0 :
						_window.insstr (i, 0, ">")
					else :
						_window.insstr (i, 0, "<")
		
		if self._messages_touched is not False :
			_message_index = 0
			_window.attrset (_color_message)
			for (_message_timestamp, _message_prefix, _message_text) in _messages :
				_message_line = _window_lines - _message_index - 1
				_window.move (_message_line, 0)
				_window.clrtoeol ()
				_window.insstr ((_message_prefix + " [..] " + _message_text) .encode ("utf-8"))
				_message_index += 1
			_window.move (_window_lines - 1, _max_columns - 1)
		
		if (_cursor_line - _head_line) >= 0 and (_cursor_line - _head_line) < _max_lines and \
				(_cursor_column - _head_column) >= 0 and (_cursor_column - _head_column) < (_max_columns - 1) :
			_window.move (_cursor_line - _head_line, _cursor_column - _head_column + 1)
		else :
			_window.move (_max_lines - 1, _max_columns - 1)
		
		_window.noutrefresh ()
		
		curses.doupdate ()

