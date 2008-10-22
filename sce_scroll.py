
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
		self._touched = False
	
	def is_touched (self) :
		return self._touched
	
	def reset_touched (self) :
		self._touched = False
	
	def get_length (self) :
		if self._lines == None :
			return 0
		return len (self._lines)
	
	def select (self, _index) :
		if self._lines == None :
			return u''
		return self._lines[_index]
	
	def update (self, _index, _string) :
		self._touched = True
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines[_index] = _string
	
	def append (self, _string) :
		self._touched = True
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.append (_string)
	
	def include_before (self, _index, _string) :
		self._touched = True
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.insert (_index, _string)
	
	def include_after (self, _index, _string) :
		self._touched = True
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.insert (_index + 1, _string)
	
	def exclude (self, _index) :
		self._touched = True
		if self._lines == None :
			return
		del self._lines[_index]
		if len (self._lines) == 0 :
			self._lines = None
	
	def exclude_all (self) :
		self._touched = True
		self._lines = None
	
	def include_all_before (self, _index, _strings) :
		self._touched = True
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.insert (_index, unicode (_string))
			_index += 1
	
	def include_all_after (self, _index, _strings) :
		self._touched = True
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.insert (_index + 1, unicode (_string))
			_index += 1
	
	def append_all (self, _string) :
		self._touched = True
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.append (unicode (_string))
	
	def split (self, _index, _column) :
		self._touched = True
		if self._lines == None :
			self._lines = [u'']
		if (_column == 0) :
			self._lines.insert (_index, u'')
		else :
			_line = self._lines[_index]
			self._lines[_index] = _line[: _column]
			self._lines.insert (_index + 1, _line[_column :])
	
	def unsplit (self, _index) :
		self._touched = True
		if self._lines == None :
			return
		_line_0 = self._lines[_index]
		_line_1 = self._lines[_index + 1]
		_line = _line_0 + _line_1
		del self._lines[_index + 1]
		self._lines[_index] = _line
	
	def insert (self, _index, _column, _string) :
		self._touched = True
		if self._lines == None :
			self._lines = [u'']
		_line = self._lines[_index]
		if (_column == 0) :
			_line = unicode (_string) + _line
		elif (_column < len (_line)) :
			_line = _line[: _column] + unicode (_string) + _line[_column :]
		elif (_column == len (_line)) :
			_line = _line + unicode (_string)
		else :
			_line = _line + (' ' * (_column - len (_line))) + unicode (_string)
		self._lines[_index] = _line
	
	def delete (self, _index, _column, _length) :
		self._touched = True
		if self._lines == None :
			self._lines = [u'']
		_line = self._lines[_index]
		if (_column > len (_line)) :
			pass
		elif (_column + _length) >= len (_line) :
			_line = _line[: _column]
		elif _column == 0 :
			_line = _line[_length :]
		else :
			_line = _line[: _column] + _line[_column + _length :]
		self._lines[_index] = _line
#
