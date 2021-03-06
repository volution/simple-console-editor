
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

if __name__ == '__main__' :
	raise Exception ()


import os
import sys
import traceback


def main (_main) :
	
	#_terminal_stream = open ('/dev/tty', 'rwb')
	_terminal_stream = sys.stderr
	
	if not os.isatty (_terminal_stream.fileno ()) :
		print >> _terminal_stream, '[ee]', 'invalid terminal;  expected a TTY;  aborting!'
		sys.exit (1)
	
	_transcript_stream = _terminal_stream
	_transcript = Transcript (_transcript_stream)
	
	_arguments = sys.argv[1:]
	
	try :
		_error = _main (_arguments, _terminal_stream, _transcript)
	except :
		_error = sys.exc_info ()
		_traceback = traceback.format_exception (_error[0], _error[1], _error[2])
		_error = (_error[1], _traceback)
	
	if _error is None :
		sys.exit (0)
	elif _error is True :
		sys.exit (0)
	elif _error is False :
		sys.exit (1)
	elif isinstance (_error, tuple) and (len (_error) == 2) :
		print >> _transcript_stream, '[ee]', 'failed!'
		print >> _transcript_stream, '[--]', '----------------------------------------'
		for _line in _error[1] :
			print >> _transcript_stream, _line.strip ('\n\r')
		print >> _transcript_stream, '[--]', '----------------------------------------'
		sys.exit (1)
	else :
		raise Exception ('86d46dd2', _error)
	
	raise Exception ('019db0ea')


class Transcript :
	
	def __init__ (self, _stream) :
		self._stream = _stream
	
	def error (self, _format, *_parts) :
		return self._push ('[ee]', _format, _parts)
	
	def warning (self, _format, *_parts) :
		return self._push ('[ww]', _format, _parts)
	
	def informative (self, _format, *_parts) :
		return self._push ('[ii]', _format, _parts)
	
	def debugging (self, _format, *_parts) :
		return self._push ('[dd]', _format, _parts)
	
	def _push (self, _prefix, _format, _parts) :
		_message = _format % _parts
		print >> self._stream, _prefix, _message
