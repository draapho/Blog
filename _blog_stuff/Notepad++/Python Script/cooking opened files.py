import os;
import sys;
from Npp import *

##
# @brief Do some operate about the file
#
def run_menu_command():
	##### Space to TAB
	# Edit->Blank Operations
	notepad.runMenuCommand("Blank Operations", "Trim Trailing Space")
	# notepad.runMenuCommand("Blank Operations", "TAB to Space")
	notepad.runMenuCommand("Blank Operations", "Space to TAB (All)")

	##### Convert Encoding to UTF-8
	# notepad.runMenuCommand("Encoding", "Encode in ANSI")
	# notepad.runMenuCommand("Encoding", "Convert to UTF-8")

	return

##
# @brief Find and operate files opened at notepad
# There are something wrong about notepad.getFiles()!!!
#
def operate_file_in_notepad():
	file_list = notepad.getFiles()
	for file in file_list:
		fn = file[0]
		notepad.activateFile(fn)
		run_menu_command()

operate_file_in_notepad()
