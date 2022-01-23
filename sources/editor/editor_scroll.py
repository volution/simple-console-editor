
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *

import common


class Scroll (common.Scroll) :
	
	def __init__ (self) :
		common.Scroll.__init__ (self)
	
	def split (self, _index, _column) :
		if self._sealed :
			raise Exception ("[fe5d770f]")
		if self._lines is None :
			self._lines = [(0, "")]
		if _column == 0 :
			self._lines.insert (_index, (0, ""))
		else :
			_revision_1 = self._updated_next ()
			_revision_2 = self._updated_next ()
			_string = self._lines[_index][1]
			_line_1 = (_revision_1, _string[: _column])
			_line_2 = (_revision_2, _string[_column :])
			self._lines[_index] = _line_1
			self._lines.insert (_index + 1, _line_2)
	
	def unsplit (self, _index) :
		if self._sealed :
			raise Exception ("[3177f7b2]")
		if self._lines is None :
			return
		_revision = self._updated_next ()
		_line_1 = self._lines[_index]
		_line_2 = self._lines[_index + 1]
		_string = _line_1[1] + _line_2[1]
		_line = (_revision, _string)
		del self._lines[_index + 1]
		self._lines[_index] = _line
	
	def insert (self, _index, _column, _string) :
		if self._sealed :
			raise Exception ("[9f4e8ab5]")
		if self._lines is None :
			self._lines = [(0, "")]
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line_string = self._lines[_index][1]
		if (_column == 0) :
			_line_string = _string + _line_string
		elif (_column < len (_line_string)) :
			_line_string = _line_string[: _column] + _string + _line_string[_column :]
		elif (_column == len (_line_string)) :
			_line_string = _line_string + _string
		else :
			_line_string = _line_string + (" " * (_column - len (_line_string))) + _string
		_line = (_revision, _line_string)
		self._lines[_index] = _line
	
	def delete (self, _index, _column, _length) :
		if self._sealed :
			raise Exception ("[5a90f1fe]")
		if self._lines is None :
			self._lines = [(0, "")]
		_line_string = self._lines[_index][1]
		if (_column > len (_line_string)) :
			return
		elif (_column + _length) >= len (_line_string) :
			_line_string = _line_string[: _column]
		elif _column == 0 :
			_line_string = _line_string[_length :]
		else :
			_line_string = _line_string[: _column] + _line_string[_column + _length :]
		_revision = self._updated_next ()
		_line = (_revision, _line_string)
		self._lines[_index] = _line

