
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division


__all__ = [
		
		"xrange_",
		"basestring_",
		"unicode_",
		"unichr_",
		"thread",
		
		"sys",
		"os",
		
		"codecs",
		"curses",
		"errno",
		"fcntl",
		"hashlib",
		"itertools",
		"locale",
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
		
		thread = __import__ ("thread")
		
	else :
		raise Exception ("[c5badf13]", sys.version_info.major, sys.version_info.minor)
	
elif sys.version_info.major == 3 :
	if sys.version_info.minor >= 6 :
		
		xrange_ = range
		basestring_ = str
		unicode_ = str
		unichr_ = chr
		
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
import locale
import os
import re
import subprocess
import time
import traceback
import uuid

