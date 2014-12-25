

Pager examples
==============


Invocation syntax
-----------------

::

	./scripts/pager <pattern>
	./scripts/pager <pattern> <prefix> <anchor> <suffix> <data>

The four arguments are:

	* ``<pattern>`` a regular expression (``^(pub...`` in the next example) which should match parts of the line that should be highligted;
	* ``<prefix>`` a substitution template (``\g<1>`` in the next example) that will be part of the normal text, right before the anchor;
	* ``<anchor>`` a substitution template (``[\g<2>]`` in the next example) that will be highlighted anchor;
	* ``<suffix>`` a substitution template (a space in the next example) that will be part of the normal text, right after the anchor;
	* ``<data>`` a substitution template (``\g<2>`` in the next example) that constitutes the data to be outputed if the current anchor is selected;

Notes:

	* The matched part of the string is replaced by concatenating the expansion of prefix, anchor and suffix.
	* Having both a prefix, suffix, and anchor, allows the user to make "contextual" matches, like in the next example we identify key identifiers as hexademical strings, but only those that appear in the first part of a line starting with ``pub``, but ignoring the GPG key type (which in it turn resembles a hexadecimal string).
	* Having a different data template, allows the user to present perhaps a shorter version of the data, but still output it in full.
	* The syntax of both the regular expressions and substitution patterns are those from the ``re`` Python 2 library.
	* The regular expression is executed over individual lines, therefore the match will not "wrap" at the line end.
	* Obviously you can have more than one highlight per line.


Choose GPG key identifiers
--------------------------

Run the following script (by pasting it in your shell): ::

	gpg2 --list-keys \
	| ./scripts/pager '^(pub +[0-9A-Z]+/)([0-9A-F]+) ' '\g<1>' '[\g<2>]' ' ' '\g<2>' \
	| cat

Once the pager starts do the following:

	* press ``Tab`` to move the cursor to the next highlighted key identifier;  (the highlights are in yellow;)
	* press ``Enter`` to select the highlighed key identifier, once you are "over" it with the cursor;  (the selected highlights are in red;)
	* continue to press ``Tab`` to find other key identifiers, and ``Enter`` to select them;
	* to unselect a highlighted key identifier press ``Enter`` once you are "over" it with the cursor;
	* press ``Ctrl+X`` to exit;  (the selected key identifiers are printed to the standard output, sorted in lexicographical order;)


Miscellaneous
-------------

Advanced "tricks":

	* you can run various commands by pressing ``Ctrl+R``;
	* one of those commands is ``filter <<pattern>> <<context-lines>>``, which will show only those lines matching the pattern, plus the choosen number of lines before and after the match;  (to clear the filter just run ``filter``;)
