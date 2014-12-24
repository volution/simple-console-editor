
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
		self._filter_re = None
		self._filtered_lines = None
		self._highlights_re = None
		self._highlights_string_prefix_sub = None
		self._highlights_string_anchor_sub = None
		self._highlights_string_suffix_sub = None
		self._highlights_data_sub = None
		self._cache = dict ()
	
	def is_touched (self) :
		return self._touched
	
	def reset_touched (self) :
		self._touched = False
	
	def force_touched (self) :
		self._touched = True
	
	def get_length (self) :
		if self._lines is None :
			_length = 0
		elif self._filtered_lines is not None :
			if self._filtered_lines is False :
				self._filter_apply ()
			_length = len (self._filtered_lines)
		else :
			_length = len (self._lines)
		return _length
	
	def select (self, _index) :
		_string = self._select_line (_index)
		if _string is None :
			return u''
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
	
	def _select_line (self, _index) :
		if self._lines is None :
			_string = None
		elif self._filtered_lines is not None :
			if self._filtered_lines is False :
				self._filter_apply ()
			_string = self._filtered_lines[_index]
		else :
			_string = self._lines[_index]
		return _string
	
	def update (self, _index, _string) :
		raise Exception ()
	
	def append (self, _string) :
		self._touched = True
		_string = self._coerce (_string)
		if self._lines is None :
			self._lines = [_string]
		else :
			self._lines.append (_string)
		self._filtered_lines = False
	
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
		if self._lines is None :
			self._lines = []
		for _string in _strings :
			_string = self._coerce (_string)
			self._lines.append (_string)
		self._filtered_lines = False
	
	def split (self, _index, _column) :
		raise Exception ()
	
	def unsplit (self, _index) :
		raise Exception ()
	
	def insert (self, _index, _column, _string) :
		raise Exception ()
	
	def delete (self, _index, _column, _length) :
		raise Exception ()
	
	def set_filter (self, _re) :
		if _re is None :
			self._filter_re = None
		else :
			self._filter_re = re.compile (_re)
		self._filtered_lines = False
	
	def _filter_apply (self) :
		if self._filter_re is None :
			self._filtered_lines = self._lines
			return
		_filter_re = self._filter_re
		_filtered_lines = list ()
		for _line in self._lines :
			_match = _filter_re.search (_line)
			if _match is not None :
				_filtered_lines.append (_line)
		self._filtered_lines = _filtered_lines
	
	def highlights (self, _index) :
		_string = self._select_line (_index)
		if _string is None :
			return []
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
	
	def set_highlights (self, _re, _strings_sub, _data_sub) :
		self._highlights_re = re.compile (_re)
		self._highlights_string_prefix_sub = _strings_sub[0]
		self._highlights_string_anchor_sub = _strings_sub[1]
		self._highlights_string_suffix_sub = _strings_sub[2]
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
		_string_prefix_sub = self._highlights_string_prefix_sub
		_string_anchor_sub = self._highlights_string_anchor_sub
		_string_suffix_sub = self._highlights_string_suffix_sub
		_data_sub = self._highlights_data_sub
		if _re is None :
			return (_line, [])
		_highlights_1 = []
		for _match in _re.finditer (_line) :
			_highlight_string_prefix = _match.expand (_string_prefix_sub)
			_highlight_string_anchor = _match.expand (_string_anchor_sub)
			_highlight_string_suffix = _match.expand (_string_suffix_sub)
			_highlight_strings = (_highlight_string_prefix, _highlight_string_anchor, _highlight_string_suffix)
			_highlight_data = _match.expand (_data_sub)
			_highlight_range = (_match.start (), _match.end ())
			_highlight = (_highlight_range, _highlight_strings, _highlight_data)
			_highlights_1.append (_highlight)
		_buffer = []
		_input_marker = 0
		_output_marker = 0
		_highlight_marker = 0
		_highlights_2 = []
		for _highlight in _highlights_1 :
			_highlight_range_begin = _highlight[0][0]
			_highlight_range_end = _highlight[0][1]
			_highlight_string_prefix = _highlight[1][0]
			_highlight_string_anchor = _highlight[1][1]
			_highlight_string_suffix = _highlight[1][2]
			_highlight_data = _highlight[2]
			_buffer.append (_line[_input_marker : _highlight_range_begin])
			_output_marker += _highlight_range_begin - _input_marker
			_input_marker += _highlight_range_end
			_buffer.append (_highlight_string_prefix)
			_buffer.append (_highlight_string_anchor)
			_buffer.append (_highlight_string_suffix)
			_highlight_anchor_begin = _output_marker + len (_highlight_string_prefix)
			_highlight_anchor_end = _highlight_anchor_begin + len (_highlight_string_anchor)
			_output_marker = _highlight_anchor_end + len (_highlight_string_suffix)
			_highlight = (
					_highlight_anchor_begin, _highlight_anchor_end,
					_highlight_string_anchor, _highlight_data)
			_highlights_2.append (_highlight)
		_buffer.append (_line[_input_marker:])
		_line = ''.join (_buffer)
		return (_line, _highlights_2)
	
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
