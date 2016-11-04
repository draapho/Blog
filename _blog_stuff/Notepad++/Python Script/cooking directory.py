import os;
import sys;
from Npp import *

##
# @brief set the path to cook
path="D:\\Users\\draap\\Desktop\\cooking"

##
# @brief Do some operate about the file
#
def run_menu_command():
	##### Space to TAB
	# Edit->Blank Operations
	notepad.runMenuCommand("Blank Operations", "Trim Trailing Space")
	# notepad.runMenuCommand("Blank Operations", "TAB to Space")
	#notepad.runMenuCommand("Blank Operations", "Space to TAB (All)")

	##### Convert Encoding to UTF-8
	# notepad.runMenuCommand("Encoding", "Encode in ANSI")
	# notepad.runMenuCommand("Encoding", "Convert to UTF-8")

	return

##
# @brief Find and operate files opened at disk
#
def operate_file_in_path(file_path = path):
	for root, dirs, file in os.walk(file_path):
		for fn in file:
			if fn[-2:] == '.c' or fn[-2:] == '.h' or fn[-3:] == '.py' :
				notepad.open(root + "\\" + fn)
				run_menu_command()
				notepad.save()
				notepad.close()

operate_file_in_path()

