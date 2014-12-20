
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
		_column = _cursor.get_column ()
		_scroll.split (_line, _view.select_real_column (_line, _column))
		_string = _scroll.select (_line)
		_prefix = []
		for _char in _string :
			if _char == ' ' :
				_prefix.append (_char)
			elif _char == '\t' :
				_prefix.append (_char)
			else :
				break
		_prefix = ''.join (_prefix)
		_scroll.insert (_line + 1, 0, _prefix)
		_column = _view.compute_visual_length (_prefix)
		_cursor.increment_line (1)
		_cursor.set_column (_column)
	
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
