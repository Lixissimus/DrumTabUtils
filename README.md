DrumTabUtils
============

Drum tabs are normally written like plain text. This can be a mess, since one drum tab line consists of many plain text lines. E.g. dublicating one bar results in copy and pasting each line of the bar.
DrumTabUtils tackles this problem by interpreting several plain text lines as one tab line. This makes it easy to dublicate or insert new empty bars. It has an understanding of the length of bars, so when you insert an empty bar, it will have the same number of units as the previous one.
It also comes with a number of pre-defined snippets to support you in creating the first bar of you tabs.


How to use it
-------------

To execute a task in DrumTabUtils, it needs two steps:

1. Select the bar, on which the command is executed on
	- Set the cursor into the bar you want to manipulate
	- From this position, select all the lines of the bar, that should be included in the execution. This can be done by using Shift + Arrow keys or just the mouse.
2. Select the actual command
	- Every command can be executed with the shortcut Ctrl + j, Ctrl + X, where X stands for one possibility from the command list below


Commands
--------

Select each line of a bar
	- Shortcut: Ctrl + j, Ctrl + s
	- This command selects each line (that was included in the selection, see "How to use it - Step 1") of a bar. Possible usecases are copying a whole bar or writing unisono parts.

Insert an empty bar
	- Shortcut: Ctrl + j, Ctrl + n
	- This command inserts an empty bar after the selected one with as many lines as selected. The newly inserted bar has the same length as the previous one.

Dublicate a bar
	- Shortcut: Ctrl + j, Ctrl + d
	- This command dublicates a bar and inserts it after the selected one. 

Remove a bar
	- Shortcut: Ctrl + j, Ctrl + r
	- This command removes the selected lines of the bar or the whole bar, if all lines were selected.


Snippets
--------

To simplify the creation of the first bar, some snippets are provided.

4/4 	-> inserts an empty bar with the instruments HH, SN, BD
4/4_3 	-> inserts an empty bar with the instruments HH, SN, BD with a triplet feeling

If you do not find the kind of bar you need, you can easily write you own one. Since all commands have an understanding of bars separated by "|", they work with any length of bars.


Useful Sublime commands and packages
------------------------------------

Sublime already provides many useful commands to write drum tabs. If you are not familiar with most of the standard commands, I highly recommend reading some documentation or the Default-key-bindings file. 

However, very useful can be the following ones:
- Ctrl + Shift + d dublicates a whole line and inserts it after the selected one
- Ctrl + Shift + up/down moves a whole line













