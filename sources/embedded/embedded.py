
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *


class Embedded (object) :
	
	def __init__ (self) :
		
		_uname = os.uname ()
		self._uname_node = _uname[1]
		self._uname_system = _uname[0]
		self._uname_release = _uname[2]
		self._uname_version = _uname[3]
		self._uname_machine = _uname[4]
		
		self._uname_fingerprint = None
	
	def project_url (self) :
		return "https://github.com/volution/simple-console-editor"
	
	def build_target (self) :
		return """@{SCE_BUILD_TARGET}"""
	
	def build_version (self) :
		return """@{SCE_BUILD_VERSION}"""
	
	def build_number (self) :
		return """@{SCE_BUILD_NUMBER}"""
	
	def build_timestamp (self) :
		return """@{SCE_BUILD_TIMESTAMP}"""
	
	def build_sources_hash (self) :
		return """@{SCE_BUILD_SOURCES_HASH}"""
	
	def build_git_hash (self) :
		return """@{SCE_BUILD_GIT_HASH}"""
	
	def uname_node (self) :
		return self._uname_node
	
	def uname_system (self) :
		return self._uname_system
	
	def uname_release (self) :
		return self._uname_release
	
	def uname_machine (self) :
		return self._uname_machine
	
	def uname_fingerprint (self) :
		if self._uname_fingerprint is not None :
			return self._uname_fingerprint
		_hasher = hashlib.sha256 ()
		_chunks = [
				"98ff673c677ffaeb481ce53a8deef977",
				self._uname_node,
				self._uname_system,
				self._uname_release,
				self._uname_version,
				self._uname_machine,
			]
		for _chunk in _chunks :
			_hasher.update (_chunk.encode ("utf-8"))
			_hasher.update (b"\0")
		self._uname_fingerprint = _hasher.hexdigest () [:32]
		return self._uname_fingerprint
	
	def write_version (self, _stream) :
		_lines = [
				"* version       : %s" % (self.build_version (),),
				"* build target  : %s, %s, python-%d.%d.%d-%s" % (self.build_target (), sys.platform, sys.version_info[0], sys.version_info[1], sys.version_info[2], sys.version_info[3]),
				"* build number  : %s, %s" % (self.build_number (), self.build_timestamp (),),
				"* code & issues : %s" % (self.project_url (),),
				"* sources git   : %s" % (self.build_git_hash (),),
				"* sources hash  : %s" % (self.build_sources_hash (),),
				"* uname node    : %s" % (self.uname_node (),),
				"* uname system  : %s, %s, %s" % (self.uname_system (), self.uname_release (), self.uname_machine (),),
				"* uname hash    : %s" % (self.uname_fingerprint (),),
				"",
			]
		_buffer = "\n".join (_lines)
		_stream.write (_buffer.encode ("utf-8"))

