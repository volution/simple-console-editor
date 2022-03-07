
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division


__all__ = [
		
		"xrange_",
		"basestring_",
		"unicode_",
		"unichr_",
		"bytechr_",
		"thread",
		
		"sys",
		"os",
		
		"codecs",
		"curses",
		"errno",
		"fcntl",
		"hashlib",
		"itertools",
		"os",
		"re",
		"subprocess",
		"time",
		"traceback",
		"uuid",
		
	]


import sys
import os


if sys.version_info.major == 2 :
	if sys.version_info.minor >= 7 :
		
		xrange_ = xrange
		basestring_ = basestring
		unicode_ = unicode
		unichr_ = unichr
		bytechr_ = chr
		
		thread = __import__ ("thread")
		
	else :
		raise Exception ("[c5badf13]", sys.version_info.major, sys.version_info.minor)
	
elif sys.version_info.major == 3 :
	if sys.version_info.minor >= 6 :
		
		xrange_ = range
		basestring_ = str
		unicode_ = str
		unichr_ = chr
		bytechr_ = lambda _code : bytes ([_code])
		
		thread = __import__ ("_thread")
		
	else :
		raise Exception ("[e88f1f9c]", sys.version_info.major, sys.version_info.minor)
	
else :
	raise Exception ("[7d6ff9ea]", sys.version_info.major, sys.version_info.minor)


import codecs
import curses
import errno
import fcntl
import hashlib
import itertools
import os
import re
import subprocess
import time
import traceback
import uuid




def _override_locale () :
	
	import locale
	
	for _locale in ["C.UTF-8", "en_US.UTF-8", "C"] :
		try :
			os.environ["LANG"] = _locale
			os.environ["LC_ALL"] = _locale
			locale.setlocale (locale.LC_ALL, _locale)
			break
		except :
			if _locale == "C" :
				raise Exception ("[b8c2b0a2]", _locale)

if True :
	_override_locale ()

