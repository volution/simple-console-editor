
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

import curses


class Handler :
	
	def __init__ (self) :
		pass
	
	def handle_key (self, _shell, _code) :
		
		if _code is None :
			return self.handle_key_unknown (_shell, 'Code:[none]')
		
		elif isinstance (_code, basestring) :
			if len (_code) == 1 :
				return self.handle_key_character (_shell, _code)
			else :
				raise Exception ('a078bdfa', _code)
		
		elif not isinstance (_code, int) :
			raise Exception ('9196652b', _code)
		
		elif _code < 0 :
			raise Exception ('5cab08de', _code)
		
		elif _code == _shell._backspace_code or _code == 8 : # Backspace
			return self.handle_key_backspace (_shell)
		elif _code == _shell._delete_code : # Delete
			return self.handle_key_delete (_shell)
		
		elif _code == 9 : # Tab
			return self.handle_key_tab (_shell)
		elif _code == 10 : # Enter
			return self.handle_key_enter (_shell)
		elif _code == 13 : # Enter
			return self.handle_key_enter (_shell)
		elif _code == 27 : # Escape
			return self.handle_key_escape (_shell)
		
		elif _code >= 0 and _code < 32 :
			return self.handle_key_control (_shell, _code)
		
		elif _code == curses.KEY_UP :
			return self.handle_key_up (_shell)
		elif _code == curses.KEY_DOWN :
			return self.handle_key_down (_shell)
		elif _code == curses.KEY_LEFT :
			return self.handle_key_left (_shell)
		elif _code == curses.KEY_RIGHT :
			return self.handle_key_right (_shell)
		
		elif _code == curses.KEY_HOME :
			return self.handle_key_home (_shell)
		elif _code == curses.KEY_END :
			return self.handle_key_end (_shell)
		
		elif _code == curses.KEY_PPAGE :
			return self.handle_key_page_up (_shell)
		elif _code == curses.KEY_NPAGE :
			return self.handle_key_page_down (_shell)
		
		elif _code == curses.KEY_IC :
			return self.handle_key_insert (_shell)
		elif _code == curses.KEY_DC :
			return self.handle_key_delete (_shell)
		
		elif _code == curses.KEY_BACKSPACE :
			return self.handle_key_backspace (_shell)
		elif _code == curses.KEY_ENTER :
			return self.handle_key_enter (_shell)
		
		elif (_code >= curses.KEY_F0) and (_code <= curses.KEY_F63) :
			return self.handle_key_function (_shell, _code - curses.KEY_F0)
		
		else :
			return self.handle_key_unknown (_shell, _code)
		
		raise Exception ('ba0402d0')
	
	def handle_key_backspace (self, _shell) :
		return self.handle_key_special (_shell, 'Backspace')
	
	def handle_key_tab (self, _shell) :
		return self.handle_key_special (_shell, 'Tab')
	
	def handle_key_enter (self, _shell) :
		return self.handle_key_special (_shell, 'Enter')
	
	def handle_key_escape (self, _shell) :
		return self.handle_key_special (_shell, 'Escape')
	
	def handle_key_delete (self, _shell) :
		return self.handle_key_special (_shell, 'Delete')
	
	def handle_key_control (self, _shell, _code) :
		return self.handle_key_special (_shell, 'Ctrl+%s' % (chr (64 + _code)))
	
	def handle_key_character (self, _shell, _character) :
		return self.handle_key_special (_shell, _character)
	
	def handle_key_up (self, _shell) :
		return self.handle_key_special (_shell, 'Up')
	
	def handle_key_down (self, _shell) :
		return self.handle_key_special (_shell, 'Down')
	
	def handle_key_left (self, _shell) :
		return self.handle_key_special (_shell, 'Left')
	
	def handle_key_right (self, _shell) :
		return self.handle_key_special (_shell, 'Right')
	
	def handle_key_home (self, _shell) :
		return self.handle_key_special (_shell, 'Home')
	
	def handle_key_end (self, _shell) :
		return self.handle_key_special (_shell, 'End')
	
	def handle_key_page_up (self, _shell) :
		return self.handle_key_special (_shell, 'Page up')
	
	def handle_key_page_down (self, _shell) :
		return self.handle_key_special (_shell, 'Page down')
	
	def handle_key_insert (self, _shell) :
		return self.handle_key_special (_shell, 'Insert')
	
	def handle_key_function (self, _shell, _code) :
		return self.handle_key_special (_shell, 'F%d' % (_code))
	
	def handle_key_special (self, _shell, _code) :
		return self.handle_key_unknown (_shell, _key)
	
	def handle_key_unknown (self, _shell, _key) :
		_shell.notify ('Unhandled key [%s]; ignoring.', _key)
		return False
#
