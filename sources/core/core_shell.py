
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

import curses
import locale
import os
import sys
import time
import traceback


class Shell :
	
	def __init__ (self) :
		self._view = None
		self._handler = None
		self._messages = []
		self._messages_touched = False
		self._max_message_lines = 10
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
		
		locale.setlocale (locale.LC_ALL, '')
		
		curses.setupterm (os.environ['TERM'], _terminal_descriptor)
		
		self._window = curses.initscr ()
		
		curses.start_color ()
		curses.use_default_colors ()
		curses.init_pair (1, curses.COLOR_WHITE, -1)
		curses.init_pair (2, curses.COLOR_BLUE, -1)
		curses.init_pair (3, curses.COLOR_RED, -1)
		curses.init_pair (4, curses.COLOR_MAGENTA, -1)
		curses.init_pair (5, curses.COLOR_GREEN, -1)
		curses.init_pair (6, curses.COLOR_YELLOW, -1)
		self._color_text = curses.color_pair (1) | curses.A_NORMAL
		self._color_markup = curses.color_pair (2) | curses.A_DIM
		self._color_error = curses.color_pair (3) | curses.A_BOLD
		self._color_message = curses.color_pair (4) | curses.A_NORMAL
		self._color_input = curses.color_pair (5) | curses.A_NORMAL
		self._color_highlight = curses.color_pair (6) | curses.A_NORMAL
		
		curses.noecho ()
		curses.nonl ()
		curses.raw ()
		
		self._window.leaveok (0)
		self._window.idcok (0)
		self._window.idlok (0)
		self._window.keypad (1)
		self._window.scrollok (0)
		
		self._opened = True
		
		return None
	
	def close (self) :
		
		self._window.scrollok (1)
		self._window.keypad (0)
		self._window.clear ()
		self._window.refresh ()
		
		curses.echo ()
		curses.nl ()
		curses.noraw ()
		
		curses.endwin ()
		
		del self._window
		del self._color_text
		del self._color_markup
		del self._color_message
		del self._color_input
		
		self._opened = False
		
		return None
	
	def scan (self) :
		_window = self._window
		_code = _window.getch ()
		if _code < 0 :
			pass
		elif (_code >= 0) and (_code < 32) :
			pass
		elif (_code >= 32) and (_code < 127) :
			_code = unicode (chr (_code))
		elif _code == 127 :
			pass
		elif (_code >= 128) and (_code < 192) :
			_code = None
		elif (_code >= 192) and (_code < 194) :
			_code = None
		elif (_code >= 194) and (_code < 224) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code = (chr (_code_1) + chr (_code_2)) .decode ('utf-8')
		elif (_code >= 224) and (_code < 240) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code_3 = _window.getch ()
			_code = (chr (_code_1) + chr (_code_2) + chr (_code_3)) .decode ('utf-8')
		elif (_code >= 240) and (_code < 245) :
			_code_1 = _code
			_code_2 = _window.getch ()
			_code_3 = _window.getch ()
			_code_4 = _window.getch ()
			_code = (chr (_code_1) + chr (_code_2) + chr (_code_3) + chr (_code_4)) .decode ('utf-8')
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
	
	def flush (self) :
		curses.flushinp ()
	
	def alert (self) :
		curses.beep ()
	
	def notify (self, _format, *_arguments) :
		_message = _format % _arguments
		self._messages.insert (0, (('[%s]' % (time.strftime ('%H:%M:%S'))), _message))
		del self._messages[self._max_message_lines :]
		self._messages_touched = True
		if not self._opened :
			print >> self._terminal, '[..]', _message
	
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
			_request = _request[:_request_max_length - 6] + ' [...]'
		_window.attrset (self._color_input)
		_window.move (_request_line, 0)
		_window.clrtoeol ()
		_window.insstr (('[??] ' + _request) .encode ('utf-8'))
		_buffer = []
		_inputs = self._inputs
		_inputs_count = len (_inputs)
		_input = _inputs_count
		while True :
			_string = u''.join (_buffer)
			_response = _string
			if len (_response) > _response_max_length :
				_response_drop = len (_response) - _response_max_length + 6
				_response = '[...] ' + _response[_response_drop:]
			_window.move (_response_line, 0)
			_window.clrtoeol ()
			_window.insstr (('[>>] ' + _response) .encode ('utf-8'))
			_window.move (_response_line, 5 + len (_response))
			_window.refresh ()
			_code = self.scan ()
			if _code is None :
				curses.beep ()
			elif isinstance (_code, basestring) :
				_buffer.append (_code)
			elif not isinstance (_code, int) :
				curses.beep ()
			elif (_code == self._backspace_code) or (_code == 8) :
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
			elif (_code == curses.KEY_UP) or (_code == curses.KEY_DOWN) :
				if _inputs_count == 0 :
					curses.beep ()
					continue
				if _code == curses.KEY_UP :
					_input -= 1
				elif _code == curses.KEY_DOWN :
					_input += 1
				_buffer = []
				if (_input == -1) or (_input == _inputs_count) :
					curses.beep ()
					continue
				if _input < 0 :
					_input = _inputs_count - 1
				if _input > _inputs_count :
					_input = 0
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
		_color_highlight = self._color_highlight
		
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
			_column = 0
			if _line < _lines :
				_window.attrset (_color_markup)
				if _view.select_is_tagged (_line) :
					_window.insstr (i, _column, '|')
					_column += 1
				else :
					_window.insstr (i, _column, ' ')
					_column += 1
				_buffer = _view.select_visual_string (_line, _head_column, _tail_column)
				for _code in _buffer :
					if isinstance (_code, basestring) :
						_window.insstr (i, _column, _code.encode ('utf-8'))
						_column += len (_code)
					elif _code == -1 :
						_window.attrset (_color_text)
					elif _code == -2 :
						_window.attrset (_color_markup)
					elif _code == -3 :
						_window.attrset (_color_error)
					elif _code == -4 :
						_window.attrset (_color_highlight)
					else :
						_window.insstr (_i, _column, '?')
						_column += 1
			else :
				_window.attrset (_color_markup)
				_window.insstr (i, _column, '~~~~')
				break
		
		_window.move (_cursor_line - _head_line, _cursor_column - _head_column + 1)
		
		if _messages_touched :
			_index = 0
			_window.attrset (_color_message)
			for (_time, _text) in _messages :
				_line = _max_lines - _index - 1
				_window.move (_line, 0)
				_window.clrtoeol ()
				_window.insstr ((_time + ' [..] ' + _text) .encode ('utf-8'))
				_index += 1
			_window.move (_max_lines - 1, _max_columns - 1)
		
		_window.refresh ()
#
