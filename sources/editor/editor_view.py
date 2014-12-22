
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

import core

from editor_scroll import Scroll


class View (core.View) :
	
	def __init__ (self) :
		core.View.__init__ (self)
		self._scroll = Scroll ()
		self._mark = core.Mark ()
		self._mark_enabled = False
		self._tab_columns = 4
		self._limit_columns = 128
		try :
			import os
			_limit_columns = int (os.getenv ('SCE_LIMIT_COLUMNS'))
			if _limit_columns >= 0 :
				self._limit_columns = _limit_columns
		except :
			pass
		self._visual_cache = dict ()
	
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
		_real_string = self._scroll.select (_line)
		_cache_key = ('visual_string', _line, _head_column, _tail_column)
		_visual_string = None
		if _cache_key in self._visual_cache :
			_cache_value = self._visual_cache[_cache_key]
			_cache_real_string = _cache_value[0]
			_cache_visual_string = _cache_value[1]
			if _real_string == _cache_real_string :
				_visual_string = _cache_visual_string
		if _visual_string is None :
			_visual_string = self.compute_visual_string (_real_string, _head_column, _tail_column)
			_cache_value = (_real_string, _visual_string)
			self._visual_cache[_cache_key] = _cache_value
		return _visual_string
	
	def select_real_column (self, _line, _visual_column) :
		_real_string = self._scroll.select (_line)
		_cache_key = ('real_column', _line, _visual_column)
		_real_column = None
		if _cache_key in self._visual_cache :
			_cache_value = self._visual_cache[_cache_key]
			_cache_real_string = _cache_value[0]
			_cache_real_column = _cache_value[1]
			if _real_string == _cache_real_string :
				_real_column = _cache_real_column
		if _real_column is None :
			_real_column = self.compute_real_column (_real_string, _visual_column)
			_cache_value = (_real_string, _real_column)
			self._visual_cache[_cache_key] = _cache_value
		return _real_column
	
	def select_visual_column (self, _line, _real_column) :
		_real_string = self._scroll.select (_line)
		_cache_key = ('visual_column', _line, _real_column)
		_visual_column = None
		if _cache_key in self._visual_cache :
			_cache_value = self._visual_cache[_cache_key]
			_cache_real_string = _cache_value[0]
			_cache_visual_column = _cache_value[1]
			if _real_string == _cache_real_string :
				_visual_column = _cache_visual_column
		if _visual_column is None :
			_visual_column = self.compute_visual_column (_real_string, _real_column)
			_cache_value = (_real_string, _visual_column)
			self._visual_cache[_cache_key] = _cache_value
		return _visual_column
	
	def select_real_length (self, _line) :
		return len (self._scroll.select (_line))
	
	def select_visual_length (self, _line) :
		_real_string = self._scroll.select (_line)
		_cache_key = ('visual_length', _line)
		_visual_length = None
		if _cache_key in self._visual_cache :
			_cache_value = self._visual_cache[_cache_key]
			_cache_real_string = _cache_value[0]
			_cache_visual_length = _cache_value[1]
			if _real_string == _cache_real_string :
				_visual_length = _cache_visual_length
		if _visual_length is None :
			_visual_length = self.compute_visual_length (_real_string)
			_cache_value = (_real_string, _visual_length)
			self._visual_cache[_cache_key] = _cache_value
		return _visual_length
	
	def select_is_tagged (self, _line) :
		_cursor_line = self._cursor.get_line ()
		_mark_line = self._mark.get_line ()
		return self._mark_enabled and ((_cursor_line <= _line <= _mark_line) or (_mark_line <= _line <= _cursor_line))
	
	def refresh (self) :
		
		core.View.refresh (self)
		
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
		_limit_column = self._limit_columns
		_tab_columns = self._tab_columns
		_buffer = list ()
		_length = self.compute_visual_length (_string)
		_column = 0
		_code = 0
		_h_code = ord ('-')
		_l_code = ord ('<')
		_g_code = ord ('>')
		_e_code = ord ('!')
		_q_code = ord ('\'')
		_s_code = ord (' ')
		_last_mode = None
		_last_code = None
		_left_trimmed = _head_column > 0
		_right_trimmed = _length >= _tail_column
		if _left_trimmed :
			_head_column += 1
		if _right_trimmed :
			_tail_column -= 1
		if _left_trimmed :
			if _last_mode != -3 :
				_buffer.append (-3)
				_last_mode = -3
			_buffer.append (_l_code)
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
					if _column >= _limit_column :
						if _last_mode != -3 :
							_buffer.append (-3)
							_last_mode = -3
					else :
						if _last_mode != -1 :
							_buffer.append (-1)
							_last_mode = -1
					_buffer.append (_code)
				_column += 1
			_last_code = _code
			if _column > _tail_column :
				break
		if _column <= _tail_column and _column == _length and _last_code == 32 :
			if _last_mode != -3 :
				_buffer.append (-3)
				_last_mode = -3
			_buffer.append (_e_code)
			_column += 1
		if _column <= _tail_column and _column <= _limit_column and _head_column <= _limit_column and _tail_column >= _limit_column :
			_delta = _limit_column - max (_column, _head_column)
			if _last_mode != -1 :
				_buffer.append (-1)
				_last_mode = -1
			_buffer.extend ([_s_code] * _delta)
			_buffer.append (-2)
			_last_mode = -2
			_buffer.append (_q_code)
			_column += _delta
		if _right_trimmed :
			if _last_mode != -3 :
				_buffer.append (-3)
				_last_mode = -3
			_buffer.append (_g_code)
		_coalesced_buffer = list ()
		_coalesced_codes = list ()
		for _code in _buffer :
			if _code < 0 :
				if len (_coalesced_codes) > 0 :
					_coalesced_codes = ''.join (_coalesced_codes)
					_coalesced_buffer.append (_coalesced_codes)
					_coalesced_codes = list ()
				_coalesced_buffer.append (_code)
			else :
				_coalesced_codes.append (unichr (_code))
		if len (_coalesced_codes) > 0 :
			_coalesced_codes = ''.join (_coalesced_codes)
			_coalesced_buffer.append (_coalesced_codes)
			_coalesced_codes = list ()
		return _coalesced_buffer
#
