
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from py23 import *

from core import *
from common import *
from commands import main as commands_main

from .editor_commands import *
from .editor_handler import *
from .editor_scroll import *


def main () :
	commands_main (main_0)


def main_0 (_arguments, _terminal, _transcript) :
	
	_redirected_input = None
	if not os.isatty (0) :
		_redirected_input = os.dup (0)
	
	_redirected_output = None
	if not os.isatty (1) :
		_redirected_output = os.dup (1)
	
	_shell = _initialize (_terminal)
	if _shell is None :
		return False
	
	if _redirected_input is None and _redirected_output is None :
		if len (_arguments) > 0 :
			_load = lambda : open_command (_shell, _arguments)
		else :
			_load = lambda : True
		_store = lambda : True
	else :
		if _redirected_input is not None :
			_load = lambda : load_fd_command (_shell, [], _redirected_input)
		else :
			_load = lambda : True
		if _redirected_output is not None :
			_store = lambda : store_fd_command (_shell, [], _redirected_output)
		else :
			_store = lambda : True
	
	if not _load () :
		return False
	
	_error = _loop (_shell)
	if _error is not None :
		try :
			_dump_path = "/tmp/sce.%d.dump.%s" % (os.getuid (), uuid.uuid4 () .hex)
			_dump_stream = os.open (_dump_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC)
			if not store_fd_command (_shell, [], _dump_stream) :
				raise Exception ("[ba4ff271]")
			_transcript.error ("dumpped to scroll to `%s`...", _dump_path)
		except :
			_transcript.error ("dumping scroll failed!")
		return _error
	
	if not _store () :
		return False
	
	return None


def _loop (_shell) :
	
	_error = _shell.open ()
	if _error is not None :
		return _error
	
	_error = _shell.loop ()
	if _error is not None :
		_shell.close ()
		return _error
	
	_error = _shell.close ()
	if _error is not None :
		return _error
	
	return None


def _initialize (_terminal) :
	
	_scroll = Scroll ()
	
	_view = View ()
	_view.set_scroll (_scroll)
	
	_handler = Handler ()
	
	_handler.register_control ("X", quick_exit_command)
	_handler.register_command ("exit", exit_command)
	_handler.register_command ("quick-exit", quick_exit_command)
	
	_handler.register_control ("R", lambda _shell, _arguments : _handler.handle_command (_shell))
	
	_handler.register_control ("@", mark_command)
	_handler.register_control ("G", go_command)
	_handler.register_control ("Z", jump_command)
	_handler.register_control ("V", jump_set_command)
	_handler.register_command ("mark", mark_command)
	_handler.register_command ("go", go_command)
	_handler.register_command ("gl", go_line_command)
	_handler.register_command ("gs", go_string_command)
	_handler.register_command ("gr", go_regexp_command)
	_handler.register_command ("jump", jump_command)
	_handler.register_command ("js", jump_set_command)
	
	_handler.register_control ("Y", yank_lines_command)
	_handler.register_control ("D", copy_lines_command)
	_handler.register_control ("K", cut_lines_command)
	_handler.register_command ("yank", yank_lines_command)
	_handler.register_command ("copy", copy_lines_command)
	_handler.register_command ("cut", cut_lines_command)
	_handler.register_command ("delete", delete_lines_command)
	
	_handler.register_control ("N", replace_command)
	_handler.register_command ("replace", replace_command)
	
	_handler.register_control ("S", save_command)
	_handler.register_command ("clear", clear_command)
	_handler.register_command ("open", open_command)
	_handler.register_command ("save", save_command)
	
	_handler.register_control ("T", paste_command)
	_handler.register_command ("paste", paste_command)
	
	_handler.register_command ("load", load_command)
	_handler.register_command ("store", store_command)
	_handler.register_command ("sys", sys_command)
	_handler.register_command ("pipe", pipe_command)
	
	_shell = Shell ()
	_shell.set_view (_view)
	_shell.set_handler (_handler)
	_shell.set_terminal (_terminal)
	
	return _shell

