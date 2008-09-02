
class Scroll :
	
	def __init__ (self) :
		self._lines = None
	
	def is_empty (self) :
		return self._lines == None
	
	def get_length (self) :
		if self._lines == None :
			return 1
		return len (self._lines)
	
	def select (self, _index) :
		if self._lines == None :
			return u''
		return self._lines[_index]
	
	def update (self, _index, _string) :
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines[_index] = _string
	
	def append (self, _string) :
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.append (_string)
	
	def include_before (self, _index, _string) :
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.insert (_index, _string)
	
	def include_after (self, _index, _string) :
		_string = unicode (_string)
		if self._lines == None :
			self._lines = [_string]
		else :
			self._lines.insert (_index + 1, _string)
	
	def exclude (self, _index) :
		if self._lines == None :
			return
		del self._lines[_index]
		if len (self._lines) == 0 :
			self._lines = None
	
	def include_all_before (self, _index, _strings) :
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.insert (_index, unicode (_string))
			_index += 1
	
	def include_all_after (self, _index, _strings) :
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.insert (_index + 1, unicode (_string))
			_index += 1
	
	def append_all (self, _string) :
		if self._lines == None :
			self._lines = []
		for _string in _strings :
			self._lines.append (unicode (_string))
	
	def empty (self) :
		self._lines = None
	
	def split (self, _index, _column) :
		if self._lines == None :
			self._lines = [u'']
		if (_column == 0) :
			self._lines.insert (_index, u'')
		else :
			_line = self._lines[_index]
			self._lines[_index] = _line[: _column]
			self._lines.insert (_index + 1, _line[_column :])
	
	def unsplit (self, _index) :
		if self._lines == None :
			self._lines = [u'']
		_line_0 = self._lines[_index]
		_line_1 = self._lines[_index + 1]
		_line = _line_0 + _line_1
		del self._lines[_index + 1]
		self._lines[_index] = _line
	
	def insert (self, _index, _column, _string) :
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
