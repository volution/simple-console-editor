
class View :
	
	def __init__ (self) :
		self._cursor = Mark ()
		self._head = Mark ()
		self._tail = Mark ()
		self._max_lines = 0
		self._max_columns = 0
	
	def get_lines (self) :
		return 0
	
	def select_real_string (self, _line) :
		return ''
	
	def select_visual_string (self, _line, _head_column, _tail_column) :
		_string = self.select_real_string (_line)
		_buffer = [-1]
		for _character in _string :
			_buffer.append (ord (_character))
		return _buffer
	
	def select_real_column (self, _line, _visual_column) :
		return _visual_column
	
	def select_visual_column (self, _line, _real_column) :
		return _real_column
	
	def select_real_length (self, _line) :
		return len (self.select_real_string (_line))
	
	def select_visual_length (self, _line) :
		return len (self.select_real_string (_line))
	
	def select_is_tagged (self, _line) :
		return False
	
	def get_cursor (self) :
		return self._cursor
	
	def get_head (self) :
		return self._head
	
	def get_tail (self) :
		return self._tail
	
	def get_max_lines (self) :
		return self._max_lines
	
	def set_max_lines (self, _lines) :
		self._max_lines = _lines
	
	def get_max_columns (self) :
		return self._max_columns
	
	def set_max_columns (self, _columns) :
		self._max_columns = _columns
	
	def refresh (self) :
		
		_cursor_line = self._cursor._line
		_cursor_column = self._cursor._column
		_head_line = self._head._line
		_head_column = self._head._column
		_tail_line = self._tail._line
		_tail_column = self._tail._column
		_max_lines = self._max_lines
		_max_columns = self._max_columns
		_lines = self.get_lines ()
		
		if _lines == 0 :
			_cursor_line = 0
			_cursor_column = 0
			_head_line = 0
			_head_column = 0
			_tail_line = 0
			_tail_column = 0
			
		else :
			
			if _cursor_line < 0 :
				_cursor_line = 0
			elif _cursor_line >= _lines :
				_cursor_line = _lines - 1
			if _cursor_column < 0 :
				_cursor_column = 0
			
			if _lines <= _max_lines :
				_head_line = 0
				_tail_line = _lines - 1
			else :
				if _cursor_line <= (_head_line + 5) :
					_head_line = _cursor_line - 5
					if _head_line < 0 :
						_head_line = 0
					_tail_line = _head_line + _max_lines - 1
				if _cursor_line >= (_tail_line - 5) :
					_tail_line = _cursor_line + 5
					if _tail_line >= _lines :
						_tail_line = _lines - 1
					_head_line = _tail_line - _max_lines + 1
			
			if _tail_column - _head_column < _max_columns :
				_tail_column = _head_column + _max_columns - 1
			if _cursor_column <= (_head_column + 10) :
				_head_column = _cursor_column - 10
				if _head_column < 0 :
					_head_column = 0
				_tail_column = _head_column + _max_columns - 1
			if _cursor_column >= (_tail_column - 10) :
				_tail_column = _cursor_column + 10
				_head_column = _tail_column - _max_columns + 1
		
		self._cursor._line = _cursor_line
		self._cursor._column = _cursor_column
		self._head._line = _head_line
		self._head._column = _head_column
		self._tail._line = _tail_line
		self._tail._column = _tail_column
#


class Mark :
	
	def __init__ (self) :
		self._line = 0
		self._column = 0
	
	def get_line (self) :
		return self._line
	
	def get_column (self) :
		return self._column
	
	def set_line (self, _line) :
		self._line = _line
	
	def set_column (self, _column) :
		self._column = _column
	
	def increment_line (self, _increment) :
		self._line += _increment
	
	def increment_column (self, _increment) :
		self._column += _increment
#
