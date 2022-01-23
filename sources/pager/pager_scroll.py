
import re

import common

class Scroll (common.Scroll) :
	
	def __init__ (self) :
		common.Scroll.__init__ (self)
		self._filter_re = None
		self._filter_prefix_lines = 0
		self._filter_suffix_lines = 0
		self._filter_break = "~"
		self._filtered_lines = None
		self._filtered_revision = 0
		self._highlights_re = None
		self._highlights_string_prefix_sub = None
		self._highlights_string_anchor_sub = None
		self._highlights_string_suffix_sub = None
		self._highlights_data_sub = None
		self._highlights_classifier = None
		self._highlights_revision = 0
		self._cache = dict ()
	
	def get_length (self) :
		if self._lines is None :
			return 0
		if self._filtered_lines is not None :
			if self._filtered_lines is False or self._filtered_revision < self._updated :
				self._filter_apply ()
			return len (self._filtered_lines)
		return len (self._lines)
	
	def select_r (self, _index) :
		_line = self._select_line (_index)
		if _line is None :
			return (0, u"")
		_revision = max (_line[0], self._highlights_revision)
		_string = _line[1]
		_line = None
		_cache_key = ("line_and_highlights", _index)
		if _cache_key in self._cache :
			_cache_value = self._cache[_cache_key]
			_cache_revision = _cache_value[0]
			_cache_string = _cache_value[1]
			if _revision == _cache_revision :
				_line = (_cache_revision, _cache_string)
		if _line is None :
			_string, _highlights = self._compute_line_and_highlights (_index, _string)
			_cache_value = (_revision, _string, _highlights)
			self._cache[_cache_key] = _cache_value
			_line = (_revision, _string)
		return _line
	
	def _select_line (self, _index) :
		if self._lines is None :
			return None
		elif self._filtered_lines is not None :
			if self._filtered_lines is False or self._filtered_revision < self._updated :
				self._filter_apply ()
			return self._filtered_lines[_index]
		return self._lines[_index]
	
	def set_filter (self, _re, _prefix_lines, _suffix_lines) :
		if _re is None :
			self._filter_re = None
		else :
			self._filter_re = re.compile (_re)
		if _prefix_lines is None :
			_prefix_lines = 0
		elif _prefix_lines < 0 :
			_prefix_lines = 0
		if _suffix_lines is None :
			_suffix_lines = 0
		elif _suffix_lines < 0 :
			_suffix_lines = 0
		self._filter_prefix_lines = _prefix_lines
		self._filter_suffix_lines = _suffix_lines
		self._filtered_lines = False
	
	def _filter_apply (self) :
		_revision = self._revision_next ()
		if self._filter_re is None :
			self._filtered_lines = self._lines
			return
		_filter_re = self._filter_re
		_filter_prefix = self._filter_prefix_lines or 0
		_filter_suffix = self._filter_suffix_lines or 0
		if _filter_prefix == 0 and _filter_suffix == 0 :
			_filter_break = None
		else :
			_filter_break = self._filter_break
		_filtered_lines = list ()
		_lines = self._lines
		_line_max = len (_lines)
		_line_mark = -1
		_line_limit = -1
		for _line_index in xrange (_line_max) :
			_match = _filter_re.search (_lines[_line_index][1])
			if _match is not None :
				if _filter_break is not None and _line_mark < (_line_index - _filter_prefix - 1) :
					_filtered_lines.append (None)
				_index_perhaps_cut = True
				for _index in xrange (_line_index - _filter_prefix, _line_index + _filter_suffix + 1) :
					if _index <= _line_mark :
						continue
					elif _index >= _line_max :
						break
					if _index_perhaps_cut and _index < _line_index :
						if _lines[_index] == "" and _index > _line_considered :
							continue
						_index_perhaps_cut = False
					_filtered_lines.append ((_revision, _lines[_index][1]))
					_line_mark = _index
				_line_considered = _line_mark
				while len (_filtered_lines) > 0 and _filtered_lines[-1][1] == "" :
					del _filtered_lines[-1]
					_line_mark -= 1
		if _filter_break is not None and _line_considered < (_line_max - 1) :
			_filtered_lines.append (None)
		if _filter_break is not None :
			_line_size = 1
			for _line in _filtered_lines :
				if _line is None :
					continue
				_line_size = max (_line_size, len (_line[1]))
			_filter_break = _filter_break * max (1, _line_size / len (_filter_break))
			for _index in xrange (len (_filtered_lines)) :
				if _filtered_lines[_index] is None :
					_filtered_lines[_index] = (_revision, _filter_break)
		self._filtered_lines = _filtered_lines
		self._filtered_revision = self._updated
	
	def highlights (self, _index) :
		_line = self._select_line (_index)
		if _line is None :
			return []
		_revision = max (_line[0], self._highlights_revision)
		_string = _line[1]
		_highlights = None
		_cache_key = ("line_and_highlights", _index)
		if _cache_key in self._cache :
			_cache_value = self._cache[_cache_key]
			_cache_revision = _cache_value[0]
			_cache_highlights = _cache_value[2]
			if _revision == _cache_revision :
				_highlights = _cache_highlights
		if _highlights is None :
			_string, _highlights = self._compute_line_and_highlights (_index, _string)
			_cache_value = (_revision, _string, _highlights)
			self._cache[_cache_key] = _cache_value
		return _highlights
	
	def set_highlights (self, _re, _strings_sub, _data_sub) :
		self._highlights_revision = self._revision_next ()
		self._highlights_re = re.compile (_re)
		self._highlights_string_prefix_sub = _strings_sub[0]
		self._highlights_string_anchor_sub = _strings_sub[1]
		self._highlights_string_suffix_sub = _strings_sub[2]
		self._highlights_data_sub = _data_sub
	
	def set_highlights_classifier (self, _classifier) :
		self._highlights_revision = self._revision_next ()
		self._highlights_classifier = _classifier
	
	def flush_highlights_classifier (self) :
		self._highlights_revision = self._revision_next ()
	
	def _compute_line_and_highlights (self, _index, _line) :
		_re = self._highlights_re
		_string_prefix_sub = self._highlights_string_prefix_sub
		_string_anchor_sub = self._highlights_string_anchor_sub
		_string_suffix_sub = self._highlights_string_suffix_sub
		_classifier = self._highlights_classifier
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
			if _classifier is not None :
				_highlight_type = _classifier (_index, _highlight_anchor_begin, _highlight_anchor_end, _highlight_string_anchor, _highlight_data)
			else :
				_highlight_type = 1
			_highlight = (
					_highlight_anchor_begin, _highlight_anchor_end,
					_highlight_string_anchor, _highlight_data,
					_highlight_type)
			_highlights_2.append (_highlight)
		_buffer.append (_line[_input_marker:])
		_line = "".join (_buffer)
		return (_line, _highlights_2)

