
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

import re

class Scroll :
	
	def __init__ (self) :
		self._lines = None
		self._touched = False
		self._highlights_re = None
		self._highlights_string_sub = None
		self._highlights_data_sub = None
		self._cache = dict ()
	
	def is_touched (self) :
		return self._touched
	
	def reset_touched (self) :
		self._touched = False
	
	def force_touched (self) :
		self._touched = True
	
	def get_length (self) :
		if self._lines == None :
			return 0
		return len (self._lines)
	
	def select (self, _index) :
		if self._lines == None :
			return u''
		_string = self._lines[_index]
		_cache_key = ('line_and_highlights', _index)
		_line = None
		if _cache_key in self._cache :
			_cache_value = self._cache[_cache_key]
			_cache_string = _cache_value[0]
			_cache_line = _cache_value[1]
			if _string == _cache_string :
				_line = _cache_line
		if _line is None :
			_line, _highlights = self._compute_line_and_highlights (_string)
			_cache_value = (_string, _line, _highlights)
			self._cache[_cache_key] = _cache_value
		return _line
	
	def update (self, _index, _string) :
		raise Exception ()
	
	def append (self, _string) :
		self._touched = True
		_string = self._coerce (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.append (_string)
	
	def include_before (self, _index, _string) :
		raise Exception ()
	
	def include_after (self, _index, _string) :
		raise Exception ()
	
	def exclude (self, _index) :
		raise Exception ()
	
	def exclude_all (self) :
		raise Exception ()
	
	def include_all_before (self, _index, _strings) :
		raise Exception ()
	
	def include_all_after (self, _index, _strings) :
		raise Exception ()
	
	def append_all (self, _strings) :
		self._touched = True
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			_string = self._coerce (_string)
			self._lines.append (_string)
	
	def split (self, _index, _column) :
		raise Exception ()
	
	def unsplit (self, _index) :
		raise Exception ()
	
	def insert (self, _index, _column, _string) :
		raise Exception ()
	
	def delete (self, _index, _column, _length) :
		raise Exception ()
	
	def highlights (self, _index) :
		if self._lines == None :
			return []
		_string = self._lines[_index]
		_cache_key = ('line_and_highlights', _index)
		_highlights = None
		if _cache_key in self._cache :
			_cache_value = self._cache[_cache_key]
			_cache_string = _cache_value[0]
			_cache_highlights = _cache_value[2]
			if _string == _cache_string :
				_highlights = _cache_highlights
		if _highlights is None :
			_line, _highlights = self._compute_line_and_highlights (_string)
			_cache_value = (_string, _line, _highlights)
			self._cache[_cache_key] = _cache_value
		return _highlights
	
	def set_highlights (self, _re, _string_sub, _data_sub) :
		self._highlights_re = re.compile (_re)
		self._highlights_string_sub = _string_sub
		self._highlights_data_sub = _data_sub
		self._flush ()
	
	def highlight (self, _line, _column) :
		_highlights = self.highlights (_line)
		for _highlight in _highlights :
			if _column >= _highlight[0] and _column < _highlight[1] :
				return _highlight
		return None
	
	def _compute_line_and_highlights (self, _line) :
		_re = self._highlights_re
		_string_sub = self._highlights_string_sub
		_data_sub = self._highlights_data_sub
		if _re is None :
			return (_line, [])
		_matches = []
		for _match in _re.finditer (_line) :
			_highlight_string = _match.expand (_string_sub)
			_highlight_data = _match.expand (_data_sub)
			_highlight = (_match.start (), _match.end (), _highlight_string, _highlight_data)
			_matches.append (_highlight)
		_buffer = []
		_last_end = 0
		_new_len = 0
		_highlights = []
		for _highlight in _matches :
			_buffer.append (_line[_last_end:_highlight[0]])
			_new_len += _highlight[0] - _last_end
			_new_highlight = (
					_new_len, _new_len + len (_highlight[2]),
					_highlight[2], _highlight[3])
			_buffer.append (_highlight[2])
			_new_len += len (_highlight[2])
			_last_end = _highlight[1]
			_highlights.append (_new_highlight)
		_buffer.append (_line[_last_end:])
		_line = ''.join (_buffer)
		return (_line, _highlights)
	
	def _flush (self) :
		self._cache = dict ()
	
	def _coerce (self, _string) :
		if isinstance (_string, unicode) :
			pass
		elif isinstance (_string, str) :
			_string = unicode (_string, 'utf-8', 'replace')
		else :
			_string = unicode (str (_string))
		return _string
#
