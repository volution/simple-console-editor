
import core


class Handler (core.BasicHandler) :
	
	def __init__ (self) :
		core.BasicHandler.__init__ (self)
	
	def handle_key_backspace (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_length = _view.select_visual_length (_line)
		if _visual_column > _length :
			_cursor.set_column (_length)
		elif _visual_column > 0 :
			_real_column = _view.select_real_column (_line, _visual_column - 1)
			_scroll.delete (_line, _real_column, 1)
			_cursor.set_column (_view.select_visual_column (_line, _real_column))
		elif _line > 0 :
			_length = _view.select_visual_length (_line - 1)
			_scroll.unsplit (_line - 1)
			_cursor.increment_line (-1)
			_cursor.set_column (_length)
		else :
			_shell.alert ()
	
	def handle_key_tab (self, _shell) :
		self._insert_character (_shell, '\t')
	
	def handle_key_enter (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_scroll.split (_line, _view.select_real_column (_line, _cursor.get_column ()))
		_cursor.increment_line (1)
		_cursor.set_column (0)
	
	def handle_key_delete (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_length = _view.select_visual_length (_line)
		if _visual_column > _length :
			_cursor.set_column (_length)
		elif _visual_column < _length :
			_real_column = _view.select_real_column (_line, _visual_column)
			_scroll.delete (_line, _real_column, 1)
			_cursor.set_column (_view.select_visual_column (_line, _real_column))
		elif _line < (_scroll.get_length () - 1) :
			_scroll.unsplit (_line)
			_cursor.set_column (_length)
		else :
			_shell.alert ()
	
	def handle_key_character (self, _shell, _character) :
		self._insert_character (_shell, _character)
	
	def _insert_character (self, _shell, _character) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		_cursor = _view.get_cursor ()
		_line = _cursor.get_line ()
		_visual_column = _cursor.get_column ()
		_real_column = _view.select_real_column (_line, _visual_column)
		_scroll.insert (_line, _real_column, _character)
		_cursor.set_column (_view.select_visual_column (_line, _real_column + 1))
#
