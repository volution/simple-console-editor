
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
			self.handle_key_unknown (_shell, 'Code:WTF!')
		
		elif isinstance (_code, basestring) :
			self.handle_key_character (_shell, _code)
		
		elif not isinstance (_code, int) :
			self.handle_key_unknown (_shell, 'Code:WTF!')
		
		elif _code < 0 :
			self.handle_key_unknown (_shell, 'Code:%d' % (_code))
		
		elif _code == 8 : # Backspace
			self.handle_key_backspace (_shell)
		elif _code == 9 : # Tab
			self.handle_key_tab (_shell)
		elif _code == 10 : # Enter
			self.handle_key_enter (_shell)
		elif _code == 13 : # Enter
			self.handle_key_enter (_shell)
		elif _code == 27 : # Escape
			self.handle_key_escape (_shell)
		elif _code == 127 : # Delete
			self.handle_key_delete (_shell)
		
		elif (_code >= 0) and (_code < 32) :
			self.handle_key_control (_shell, _code)
		
		elif _code == curses.KEY_UP :
			self.handle_key_up (_shell)
		elif _code == curses.KEY_DOWN :
			self.handle_key_down (_shell)
		elif _code == curses.KEY_LEFT :
			self.handle_key_left (_shell)
		elif _code == curses.KEY_RIGHT :
			self.handle_key_right (_shell)
		
		elif _code == curses.KEY_HOME :
			self.handle_key_home (_shell)
		elif _code == curses.KEY_END :
			self.handle_key_end (_shell)
		
		elif _code == curses.KEY_PPAGE :
			self.handle_key_page_up (_shell)
		elif _code == curses.KEY_NPAGE :
			self.handle_key_page_down (_shell)
		
		elif _code == curses.KEY_IC :
			self.handle_key_insert (_shell)
		elif _code == curses.KEY_DC :
			self.handle_key_delete (_shell)
		
		elif _code == curses.KEY_BACKSPACE :
			self.handle_key_backspace (_shell)
		elif _code == curses.KEY_ENTER :
			self.handle_key_enter (_shell)
		
		elif (_code >= curses.KEY_F0) and (_code <= curses.KEY_F63) :
			self.handle_key_function (_shell, _code - curses.KEY_F0)
		
		else :
			self.handle_key_unknown (_shell, 'Code:%d' % (_code))
		
		return True
	
	def handle_key_backspace (self, _shell) :
		self.handle_key_unknown (_shell, 'Backspace')
	
	def handle_key_tab (self, _shell) :
		self.handle_key_unknown (_shell, 'Tab')
	
	def handle_key_enter (self, _shell) :
		self.handle_key_unknown (_shell, 'Enter')
	
	def handle_key_escape (self, _shell) :
		self.handle_key_unknown (_shell, 'Escape')
	
	def handle_key_delete (self, _shell) :
		self.handle_key_unknown (_shell, 'Delete')
	
	def handle_key_control (self, _shell, _code) :
		self.handle_key_unknown (_shell, 'Ctrl+%s' % (chr (64 + _code)))
	
	def handle_key_character (self, _shell, _character) :
		self.handle_key_unknown (_shell, _character)
	
	def handle_key_up (self, _shell) :
		self.handle_key_unknown (_shell, 'Up')
	
	def handle_key_down (self, _shell) :
		self.handle_key_unknown (_shell, 'Down')
	
	def handle_key_left (self, _shell) :
		self.handle_key_unknown (_shell, 'Left')
	
	def handle_key_right (self, _shell) :
		self.handle_key_unknown (_shell, 'Right')
	
	def handle_key_home (self, _shell) :
		self.handle_key_unknown (_shell, 'Home')
	
	def handle_key_end (self, _shell) :
		self.handle_key_unknown (_shell, 'End')
	
	def handle_key_page_up (self, _shell) :
		self.handle_key_unknown (_shell, 'Page up')
	
	def handle_key_page_down (self, _shell) :
		self.handle_key_unknown (_shell, 'Page down')
	
	def handle_key_insert (self, _shell) :
		self.handle_key_unknown (_shell, 'Insert')
	
	def handle_key_function (self, _shell, _code) :
		self.handle_key_unknown (_shell, 'F%d' % (_code))
	
	def handle_key_unknown (self, _shell, _key) :
		_shell.notify ('Unhandled key [%s]; ignoring.', _key)
#
