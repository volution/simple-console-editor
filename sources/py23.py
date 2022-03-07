
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
	
	if "LANG" in os.environ : del os.environ["LANG"]
	if "LC_ALL" in os.environ : del os.environ["LC_ALL"]
	if "LC_CTYPE" in os.environ : del os.environ["LC_CTYPE"]
	
	try :
		os.environ["LANG"] = "C.UTF-8"
		os.environ["LC_ALL"] = "C.UTF-8"
		os.environ["LC_CTYPE"] = "C.UTF-8"
		locale.setlocale (locale.LC_ALL, os.environ["LC_ALL"])
		locale.setlocale (locale.LC_CTYPE, os.environ["LC_CTYPE"])
	except :
		os.environ["LANG"] = "en_US.UTF-8"
		os.environ["LC_ALL"] = "en_US.UTF-8"
		os.environ["LC_CTYPE"] = "en_US.UTF-8"
		locale.setlocale (locale.LC_ALL, os.environ["LC_ALL"])
		locale.setlocale (locale.LC_CTYPE, os.environ["LC_CTYPE"])

if True :
	_override_locale ()

