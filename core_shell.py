
import curses
import locale
import traceback


class Shell :
	
	def __init__ (self) :
		self._view = None
		self._handler = None
		self._messages = []
		self._messages_touched = False
		self._max_message_lines = 10
		self._inputs = []
		self._max_input_lines = 3
	
	def get_view (self) :
		return self._view
	
	def set_view (self, _view) :
		self._view = _view
	
	def get_handler (self) :
		return self._key_handler
	
	def set_handler (self, _handler) :
		self._handler = _handler
	
	def open (self) :
		
		locale.setlocale (locale.LC_ALL, '')
		
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
		
		self._window = curses.initscr ()
		curses.raw ()
		curses.noecho ()
		curses.nonl ()
		self._window.keypad (1)
		self._window.leaveok (0)
	
	def close (self) :
		
		self._window.leaveok (1)
		self._window.keypad (0)
		curses.nl ()
		curses.echo ()
		curses.noraw ()
		curses.endwin ()
		
		del self._window
		del self._color_text
		del self._color_markup
		del self._color_message
		del self._color_input
	
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
		(_window_lines, _window_columns) = self._window.getmaxyx ()
		_line = _window_lines - self._max_input_lines
		
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
		_input = len (_inputs)
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
					_input = len (_inputs) - 1
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
		
		_window = self._window
		(_window_lines, _window_columns) = self._window.getmaxyx ()
		
		_color_text = self._color_text
		_color_markup = self._color_markup
		_color_error = self._color_error
		_color_message = self._color_message
		
		_window.erase ()
		
		_max_lines = _window_lines
		_max_columns = _window_columns - 1
		
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
		_messages_touched = self._messages_touched
		self._messages_touched = False
		
		for i in xrange (0, _max_lines) :
			_window.move (i, 0)
			_line = _head_line + i
			if _line < _lines :
				_window.attrset (_color_markup)
				if _view.select_is_tagged (_line) :
					_window.addstr ('|')
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
				_window.addstr ('~~~~')
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
