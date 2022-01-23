
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import sys


__all__ = [
		"xrange_",
		"basestring_",
		"unicode_",
		"thread_",
	]


if sys.version_info.major == 2 :
	if sys.version_info.minor >= 7 :
		
		xrange_ = xrange
		basestring_ = basestring
		unicode_ = unicode
		
		thread_ = __import__ ("thread")
		
	else :
		raise Exception (("c5badf13", sys.version_info.major, sys.version_info.minor))
	
elif sys.version_info.major == 3 :
	if sys.version_info.minor >= 6 :
		
		xrange_ = range
		basestring_ = str
		unicode_ = str
		
		thread_ = __import__ ("_thread")
		
	else :
		raise Exception (("e88f1f9c", sys.version_info.major, sys.version_info.minor))
	
else :
	raise Exception (("7d6ff9ea", sys.version_info.major, sys.version_info.minor))

