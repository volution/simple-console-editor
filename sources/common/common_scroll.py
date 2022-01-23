
from __future__ import absolute_import
from __future__ import unicode_literals


class Scroll (object) :
	
	def __init__ (self) :
		self._lines = None
		self._revision = 0
		self._updated = 0
		self._touched = 0
		self._sealed = False
	
	def get_length (self) :
		if self._lines is None :
			return 0
		return len (self._lines)
	
	def select (self, _index) :
		return self.select_r (_index) [1]
	
	def select_r (self, _index) :
		if self._lines is None :
			return (0, "")
		return self._lines[_index]
	
	def update (self, _index, _string) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			return self.append (_string)
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		self._lines[_index] = _line
	
	def append (self, _string) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			self._lines = list ()
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		self._lines.append (_line)
	
	def append_all (self, _strings) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			self._lines = list ()
		for _string in _strings :
			_revision = self._updated_next ()
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.append (_line)
	
	def include_before (self, _index, _string) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			return self.append (_string)
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		self._lines.insert (_index, _line)
	
	def include_all_before (self, _index, _strings) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			self._lines = list ()
		for _string in _strings :
			_revision = self._updated_next ()
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.insert (_index, _line)
			_index += 1
	
	def include_after (self, _index, _string) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			return self.append (_string)
		_revision = self._updated_next ()
		_string = self._coerce (_string)
		_line = (_revision, _string)
		self._lines.insert (_index + 1, _line)
	
	def include_all_after (self, _index, _strings) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			self._lines = list ()
		for _string in _strings :
			_revision = self._updated_next ()
			_string = self._coerce (_string)
			_line = (_revision, _string)
			self._lines.insert (_index + 1, _line)
			_index += 1
	
	def exclude (self, _index) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			return
		_revision = self._updated_next ()
		del self._lines[_index]
		if len (self._lines) == 0 :
			self._lines = None
	
	def exclude_all (self) :
		if self._sealed :
			raise Exception ()
		if self._lines is None :
			return
		_revision = self._updated_next ()
		self._lines = None
	
	def is_touched (self) :
		return self._touched < self._updated
	
	def reset_touched (self) :
		self._touched = self._updated
	
	def force_touched (self) :
		self._touched = 0
	
	def seal (self) :
		self._seal = True
	
	def highlights (self, _index) :
		return None
	
	def _revision_next (self) :
		_revision = self._revision + 1
		self._revision = _revision
		return _revision
	
	def _updated_next (self) :
		_revision = self._revision_next ()
		self._updated = _revision
		return _revision
	
	def _coerce (self, _string) :
		if isinstance (_string, unicode) :
			pass
		elif isinstance (_string, str) :
			_string = unicode (_string, "utf-8", "replace")
		else :
			_string = unicode (str (_string))
		return _string

