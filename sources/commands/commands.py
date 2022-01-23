
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from core.py23 import *

import os
import sys
import traceback


def main (_main) :
	
	#_terminal_stream = open ("/dev/tty", "rwb")
	_terminal_stream = sys.stderr
	
	if not os.isatty (_terminal_stream.fileno ()) :
		_terminal_stream.write ("[ee]  invalid terminal;  expected a TTY;  aborting!\n")
		sys.exit (1)
	
	_transcript_stream = _terminal_stream
	_transcript = Transcript (_transcript_stream)
	
	_arguments = sys.argv[1:]
	if len (_arguments) == 1 :
		if _arguments[0] == "-v" or _arguments[0] == "--version" :
			import embedded
			_embedded = embedded.Embedded ()
			_embedded.write_version (sys.stdout)
			sys.exit (0)
	
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
		_transcript_stream.write ("[ee]  failed!\n")
		_transcript_stream.write ("[--]  ----------------------------------------\n")
		for _line in _error[1] :
			_transcript_stream.write (_line.strip ("\n\r") + "\n")
		_transcript_stream.write ("[--]  ----------------------------------------\n")
		sys.exit (1)
	else :
		raise Exception ("86d46dd2", _error)
	
	raise Exception ("019db0ea")


class Transcript (object) :
	
	def __init__ (self, _stream) :
		self._stream = _stream
	
	def error (self, _format, *_parts) :
		return self._push ("[ee]", _format, _parts)
	
	def warning (self, _format, *_parts) :
		return self._push ("[ww]", _format, _parts)
	
	def informative (self, _format, *_parts) :
		return self._push ("[ii]", _format, _parts)
	
	def debugging (self, _format, *_parts) :
		return self._push ("[dd]", _format, _parts)
	
	def _push (self, _prefix, _format, _parts) :
		_message = _format % _parts
		self._stream.write (_prefix + "  " + _message + "\n")

