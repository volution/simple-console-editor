



.. image:: ./documentation/logo.png




--------




############################
SCE -- Simple Console Editor
############################


.. contents::
    :depth: 2
    :local:
    :backlinks: none




--------




About
=====


This is my personal plain text editor
that I have initially written in a couple of hot summer days of 2008.

Over the years I have made minor enhancements and stability improvements,
plus an initial implementation of a browser-like pager.

I have used it since the first days for all my edits,
especially for source code, scripting, configuration,
in all languages
from C to Go, Python to Scheme, Bash to Erlang,
HTML / CSS / JavaScript,
LaTeX to CommonMark,
JSON to XML,
all except Java.

The code is written in Python,
works with both Python 2.7 and 3.6+,
and is only a couple of tousand lines long,
~3.5k for the current version which includes a browser-like pager.
However on the down-side the code is quite a mess, but it gets the job done.

It has no dependencies outside
the basic Python runtime and the ``curses`` library.

It can be deployed as a simple single-file standalone executable,
and works on any POSIX-like system from Linux, to OpenBSD and OSX.




--------




Examples
========

.. contents::
    :local:
    :backlinks: none




Editor examples
~~~~~~~~~~~~~~~


Invocation syntax
-----------------


::

	sce
	sce <file>
	produce | sce | consume


In the first variant, the editor
opens with an empty buffer
and allows the user to edit it.
One can then use a command like
``save /tmp/file.txt`` to save its contents,
followed by an ``exit`` command.

To run a command just press ``Ctrl+R``
and enter the desired command.
(As an alternative to the ``exit`` command,
one can just press ``Ctrl+X``.)


In the second variant, the editor
opens the specified file
and allows the user to edit it.
One can then use a command like
``save`` to save its contents,
followed by an ``exit`` command.
(As an alternative to the ``save`` command,
one can just press ``Ctrl+S``.)


In the third variant, the editor
reads all the output produced by ``produce``,
opens with an anonymous buffer
and allows the user to edit it.
One can then use a command like
``exit`` to close the editor,
and write all the output consumed by ``consume``.
This variant basically works with pipes (or plain files)
as ``stdin`` and ``stdout``,
and does not require the usage of a temporary file.


Here are all the supported commands
(one just needs to press ``Ctrl+R`` to enter them):

* ``exit`` -- exits without asking for or executing a save;
* ``save`` or ``save /tmp/file.txt``;
* ``open /tmp/file.txt``;
* ``clear`` -- empties the current buffer;
* ``gs text`` -- search for ``text``;
  (to find the next match, just press ``Ctrl+G``;)
* ``gr regex`` -- searches for a regular expression;
  (again use ``Ctrl+G`` to find the next match;)
* ``gl number`` -- go to the line number;
* ``replace this that`` --
  it will search for the first match,
  and one has to press ``Ctrl+N`` to replace it;
  to find the next match, press ``Ctrl+N``,
  then another ``Ctrl+N`` to replace it;
* ``store`` -- stores the current selection in a temporary file;
* ``load`` -- inserts at the current cursor the stored selection from the temporary file;
* (``store`` and ``load`` work across invocations, thus allows one to copy-paste between files;)
* ``pipe command arguments...`` -- runs the command on the current file or selection, feeding it on ``stdin``, then replacing it with the result from ``stdout``;
* ``sys i command arguments...`` -- runs the command, and inserts the output from ``stdout``;
* ``sys o command arguments...`` -- runs the command, feeding the current selection on ``stdin``;
* ``copy`` -- see ``Ctrl+D``;
* ``cut`` -- see ``Ctrl+K``;
* ``yank`` -- see ``Ctrl+Y``;
* ``paste`` -- see ``Ctrl+T``;

Here are all the supported key bindings / shortcuts:

* up, down, left, right, home, end, page-up, page-down, backspace, delete -- work as expected;
* ``Ctrl+X`` -- exits the editor, if the file is untouched or already saved;
* ``Ctrl+S`` -- saves the file;
* ``Ctrl+R`` -- allows the user to enter a command;
* ``Ctrl+G`` -- go to the next match;  (as initiated by ``gs`` or ``gr``);
* ``Ctrl+N`` -- replace the current match, or go to the next replace match;  (as initiated by ``replace``;)
* ``Ctrl+Space`` -- begins a selection;  press ``Ctrl+Space`` again to end a selection;
  the selection is permanent across movements;  ``Ctrl+Space`` twice to clear the selection;
* ``Ctrl+D`` -- copy the selection into the internal buffer;
* ``Ctrl+K`` -- cut the selection into the internal buffer;
* ``Ctrl+Y`` -- pastes from the internal buffer;
* ``Ctrl+V`` -- set a jump marker on the current line;
* ``Ctrl+Z`` -- go to the previous marker, and set the current line as the new jump marker;
  (i.e. with ``Ctrl+V`` and ``Ctrl+Z`` one can easily jump between two parts of the same file;)
* ``Ctrl+T`` -- runs ``sce-paste``, which is a user provided executable,
  most likely another curses-based application,
  inserting the output from ``stdout``;
  (one could for example use ``fzf`` to provide various snippets or other "auto-completion" features;)




Pager examples
~~~~~~~~~~~~~~


Invocation syntax
-----------------


::

	produce | sce-pager <pattern> | consume
	produce | sce-pager <pattern> <prefix> <anchor> <suffix> <data> | consume


The four arguments are:

* ``<pattern>``
  -- a regular expression with captures
  (``^(pub...`` in the next example),
  which should match parts of the line that should be highligted;

* ``<prefix>``
  -- a substitution template
  (``\g<1>`` in the next example),
  that will be part of the normal text,
  right before the anchor;

* ``<anchor>``
  -- a substitution template
  (``[\g<2>]`` in the next example),
  that will be the text for the highlighted anchor;

* ``<suffix>``
  -- a substitution template
  (a space in the next example),
  that will be part of the normal text,
  right after the anchor;

* ``<data>``
  -- a substitution template
  (``\g<2>`` in the next example),
  that will be the data to be outputed
  if the current anchor is selected;


The input and output:

* the pager expects that the standard input and output
  are either a file or a pipe (in fact anything else than a TTY);
* the pager expects that the standard error is a terminal (i.e. a TTY);


Notes:

* the matched part of the string
  is replaced by concatenating the expansion of prefix, anchor and suffix;

* having both a prefix, suffix, and anchor,
  allows the user to make "contextual" matches,
  like in the next example we identify key identifiers as hexademical strings,
  but only those that appear in the first part of a line starting with ``pub``,
  but ignoring the GPG key type (which in it turn resembles a hexadecimal string);

* having a different data template,
  allows the user to present perhaps a shorter version of the data,
  but still output it in full;

* the syntax of both the regular expressions and substitution patterns
  are those from the ``re`` Python library;

* the regular expression is executed over individual lines,
  therefore the match will not "wrap" at the line end;

* obviously you can have more than one highlight per line;




Choose GPG key identifiers
--------------------------


Run the following script (by pasting it in your shell): ::

	gpg2 --list-keys --keyid-format short \
	| sce-pager '^(pub +[0-9a-zA-Z]+/)([0-9a-fA-F]+) ' '\g<1>' '[\g<2>]' ' ' '\g<2>' \
	| cat


Once the pager starts do the following:

* press ``Tab`` to move the cursor to the next highlighted key identifier;
  (the highlights are in yellow;)

* press ``Enter`` to select the highlighed key identifier,
  once you are "over" it with the cursor;
  (the selected highlights are in red;)

* continue to press ``Tab`` to find other key identifiers,
  and ``Enter`` to select them;

* to unselect a highlighted key identifier
  press ``Enter`` once you are "over" it with the cursor;

* press ``Ctrl+X`` to exit;
  the selected key identifiers are printed
  to the standard output, sorted in lexicographical order;




Miscellaneous
-------------

Advanced "tricks":

* you can run various commands by pressing ``Ctrl+R``;

* one of those commands is ``filter <pattern> <context-lines>``,
  which will show only those lines matching the pattern,
  plus the choosen number of lines before and after the match;
  (to clear the filter just run ``filter``;)




--------




Notice
======

For details about the copyright and licensing,
please consult the `notice <./documentation/licensing/notice.txt>`__ file
in the ``documentation/licensing`` folder.
(In short the code is licensed under GPL 3 or later.)

