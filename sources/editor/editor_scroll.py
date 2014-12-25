
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

class Scroll :
	
	def __init__ (self) :
		self._lines = None
		self._revision = 0
		self._updated = 0
		self._touched = 0
	
	def get_length (self) :
		if self._lines is None :
			return 0
		return len (self._lines)
	
	def select (self, _index) :
		return self.select_r (_index) [1]
	
	def select_r (self, _index) :
		if self._lines is None :
			return (0, u'')
		return self._lines[_index]
	
	def update (self, _index, _string) :
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		if self._lines is None :
			self._lines = [_line]
		else :
			self._lines[_index] = _line
	
	def append (self, _string) :
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		if self._lines is None :
			self._lines = [_line]
		else :
			self._lines.append (_line)
	
	def include_before (self, _index, _string) :
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		if self._lines is None :
			self._lines = [_line]
		else :
			self._lines.insert (_index, _line)
	
	def include_after (self, _index, _string) :
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		if self._lines is None :
			self._lines = [_line]
		else :
			self._lines.insert (_index + 1, _line)
	
	def exclude (self, _index) :
		_revision = self._updated_next ()
		if self._lines is None :
			return
		del self._lines[_index]
		if len (self._lines) == 0 :
			self._lines = None
	
	def exclude_all (self) :
		_revision = self._updated_next ()
		self._lines = None
	
	def include_all_before (self, _index, _strings) :
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = []
		for _string in _strings :
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.insert (_index, _line)
			_index += 1
	
	def include_all_after (self, _index, _strings) :
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = []
		for _string in _strings :
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.insert (_index + 1, _line)
			_index += 1
	
	def append_all (self, _strings) :
		_revision = self._updated_next ()
		if self._lines is None :
			self._lines = []
		for _string in _strings :
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.append (_line)
	
	def split (self, _index, _column) :
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
		_revision = self._updated_next ()
		if self._lines is None :
			return
		_line_1 = self._lines[_index]
		_line_2 = self._lines[_index + 1]
		_string = _line_1[1] + _line_2[1]
		_line = (_revision, _string)
		del self._lines[_index + 1]
		self._lines[_index] = _line
	
	def insert (self, _index, _column, _string) :
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		if self._lines is None :
			self._lines = [(0, u'')]
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
	
	def highlights (self, _index) :
		return []
	
	def highlight (self, _line, _column) :
		return None
	
	def _revision_next (self) :
		_revision = self._revision + 1
		self._revision = _revision
		return _revision
	
	def _updated_next (self) :
		_revision = self._revision_next ()
		self._updated = _revision
		return _revision
	
	def is_touched (self) :
		return self._touched < self._updated
	
	def reset_touched (self) :
		self._touched = self._updated
	
	def force_touched (self) :
		self._touched = 0
	
	def _coerce (self, _string) :
		if isinstance (_string, unicode) :
			pass
		elif isinstance (_string, str) :
			_string = unicode (_string, 'utf-8', 'replace')
		else :
			_string = unicode (str (_string))
		return _string
#
