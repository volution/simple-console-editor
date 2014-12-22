
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

import os
import sys

sys.path.append (os.environ['SCE_SOURCES'])

import pager

if __name__ == '__main__' :
	_error = pager.main (sys.argv[1 :])
	if _error is not None :
		print >> sys.stderr, '[ee]', 'failed!'
		sys.exit (1)
	else :
		sys.exit (0)
else :
	raise Exception ()
