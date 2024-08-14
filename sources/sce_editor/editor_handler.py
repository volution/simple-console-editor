
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *

import sce_core

__all__ = [
		"Handler",
	]


class Handler (sce_core.BasicHandler) :
	
	def __init__ (self) :
		sce_core.BasicHandler.__init__ (self)
	
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
		elif _length == 0 and _line == 0 and _scroll.get_length () == 1 :
			_scroll.exclude (0)
		else :
			_shell.alert ()
	
	def handle_key_tab (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		if not _view.is_mark_enabled () :
			_cursor = _view.get_cursor ()
			_line = _cursor.get_line ()
			_line_string = _view.select_real_string (_line)
			_line_offset = _view.select_real_column (_line, _cursor.get_column ())
			if _line_string.startswith ("    ") :
				_line_string = "    " + _line_string
				_line_offset += 4
			else :
				_line_string = "\t" + _line_string
				_line_offset += 1
			_scroll.update (_line, _line_string)
			_line_visual = _view.select_visual_column (_line, _line_offset)
			_cursor.set_column (_line_visual)
		else :
			_mark_1_line = _view.get_mark_1 () .get_line ()
			_mark_2_line = _view.get_mark_2 () .get_line ()
			if _mark_2_line == _mark_1_line :
				_mark_2_line = _view.get_cursor () .get_line ()
			_mark_1_line, _mark_2_line = (min (_mark_1_line, _mark_2_line), max (_mark_1_line, _mark_2_line))
			for _line in xrange_ (_mark_1_line, _mark_2_line + 1) :
				_line_string = _scroll.select (_line)
				if _line_string.startswith ("    ") :
					_line_string = "    " + _line_string
				else :
					_line_string = "\t" + _line_string
				_scroll.update (_line, _line_string)
	
	def handle_key_tab_backward (self, _shell) :
		_view = _shell.get_view ()
		_scroll = _view.get_scroll ()
		if not _view.is_mark_enabled () :
			_cursor = _view.get_cursor ()
			_line = _cursor.get_line ()
			_line_string = _view.select_real_string (_line)
			_line_offset = _view.select_real_column (_line, _cursor.get_column ())
			if _line_string.startswith ("    ") :
				_line_string = _line_string[4:]
				_line_offset -= 4
			elif _line_string.startswith ("\t") :
				_line_string = _line_string[1:]
				_line_offset -= 1
			_scroll.update (_line, _line_string)
			_line_visual = _view.select_visual_column (_line, _line_offset)
			_cursor.set_column (_line_visual)
		else :
			_mark_1_line = _view.get_mark_1 () .get_line ()
			_mark_2_line = _view.get_mark_2 () .get_line ()
			if _mark_2_line == _mark_1_line :
				_mark_2_line = _view.get_cursor () .get_line ()
			_mark_1_line, _mark_2_line = (min (_mark_1_line, _mark_2_line), max (_mark_1_line, _mark_2_line))
			for _line in xrange_ (_mark_1_line, _mark_2_line + 1) :
				_line_string = _scroll.select (_line)
				if _line_string.startswith ("    ") :
					_line_string = _line_string[4:]
				elif _line_string.startswith ("\t") :
					_line_string = _line_string[1:]
				_scroll.update (_line, _line_string)
	
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
			if _char == " " :
				_prefix.append (_char)
			elif _char == "\t" :
				_prefix.append (_char)
			else :
				break
		_prefix = "".join (_prefix)
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
		elif _length == 0 and _line == 0 and _scroll.get_length () == 1 :
			_scroll.exclude (0)
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

