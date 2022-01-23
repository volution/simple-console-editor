
from __future__ import absolute_import

from .core_handler import Handler


class BasicHandler (Handler) :
	
	def __init__ (self) :
		Handler.__init__ (self)
		self._commands = dict ()
		self._controls = dict ()
		self._specials = dict ()
	
	def handle_key_up (self, _shell) :
		_shell.get_view () .get_cursor () .increment_line (-1)
		return True
	
	def handle_key_down (self, _shell) :
		_shell.get_view () .get_cursor () .increment_line (1)
		return True
	
	def handle_key_left (self, _shell) :
		_shell.get_view () .get_cursor () .increment_column (-1)
		return True
	
	def handle_key_right (self, _shell) :
		_shell.get_view () .get_cursor () .increment_column (1)
		return True
	
	def handle_key_home (self, _shell) :
		_shell.get_view () .get_cursor () .set_column (0)
		return True
	
	def handle_key_end (self, _shell) :
		_view = _shell.get_view ()
		_cursor = _view.get_cursor ()
		_cursor.set_column (_view.select_visual_length (_cursor.get_line ()))
		return True
	
	def handle_key_page_up (self, _shell) :
		_view = _shell.get_view ()
		_view.get_cursor () .increment_line (- _view.get_max_lines ())
		return True
	
	def handle_key_page_down (self, _shell) :
		_view = _shell.get_view ()
		_view.get_cursor () .increment_line (_view.get_max_lines ())
		return True
	
	def handle_key_control (self, _shell, _code) :
		if _code not in self._controls :
			return self.handle_key_unknown (_shell, "Ctrl+%s" % (chr (64 + _code)))
		_handler = self._controls[_code]
		return self._execute_handler (_shell, _handler, [])
	
	def handle_key_special (self, _shell, _code) :
		if _code not in self._specials :
			return self.handle_key_unknown (_shell, _code)
		_handler = self._specials[_code]
		return self._execute_handler (_shell, _handler, [])
	
	def handle_command (self, _shell) :
		_command = _shell.input ("Command?")
		if _command is None :
			return True
		_parts = _command.split ()
		if len (_parts) == 0 :
			return True
		if _parts[0] not in self._commands :
			_shell.notify ("Unhandled command [%s]; ignoring.", _parts[0])
			return False
		_handler = self._commands[_parts[0]]
		return self._execute_handler (_shell, _handler, _parts[1:])
	
	def _execute_handler (self, _shell, _handler, _arguments) :
		try :
			_outcome = _handler (_shell, _arguments)
			#if _outcome is None :
			#	_shell.notify ("Command [%s] failed.", _command)
		except Exception as _error :
			_shell.notify ("Unhandled exception [%s]; ignoring.", str (_error))
		except :
			_shell.notify ("Unhandled unknown exception; ignoring.")
		return True
	
	def register_command (self, _command, _handler) :
		self._commands[_command] = _handler
	
	def unregister_command (self, _command) :
		del self._commands[_command]
	
	def register_control (self, _control, _handler) :
		self._controls[ord (_control) - 64] = _handler
	
	def unregister_control (self, _control) :
		del self._controls[ord (_control) - 64]
	
	def register_special (self, _special, _handler) :
		self._specials[_special] = _handler
	
	def unregister_special (self, _special) :
		del self._specials[_special]

