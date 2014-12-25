
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

import common

class Scroll (common.Scroll) :
	
	def __init__ (self) :
		common.Scroll.__init__ (self)
	
	def split (self, _index, _column) :
		if self._sealed :
			raise Exception ()
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = [(0, u'')]
		if (_column == 0) :
			self._lines.insert (_index, (0, u''))
		else :
			_string = self._lines[_index][1]
			_line_1 = (_revision, _string[: _column])
			_line_2 = (_revision, _string[_column :])
			self._lines[_index] = _line_1
			self._lines.insert (_index + 1, _line_2)
	
	def unsplit (self, _index) :
		if self._sealed :
			raise Exception ()
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
			raise Exception ()
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = [(0, u'')]
		_string = self._coerce (_string)
		_line_string = self._lines[_index][1]
		if (_column == 0) :
			_line_string = _string + _line_string
		elif (_column < len (_line_string)) :
			_line_string = _line_string[: _column] + _string + _line_string[_column :]
		elif (_column == len (_line_string)) :
			_line_string = _line_string + _string
		else :
			_line_string = _line_string + (' ' * (_column - len (_line_string))) + _string
		_line = (_revision, _line_string)
		self._lines[_index] = _line
	
	def delete (self, _index, _column, _length) :
		if self._sealed :
			raise Exception ()
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = [(0, u'')]
		_line_string = self._lines[_index][1]
		if (_column > len (_line_string)) :
			pass
		elif (_column + _length) >= len (_line_string) :
			_line_string = _line_string[: _column]
		elif _column == 0 :
			_line_string = _line_string[_length :]
		else :
			_line_string = _line_string[: _column] + _line_string[_column + _length :]
		_line = (_revision, _line_string)
		self._lines[_index] = _line
#
