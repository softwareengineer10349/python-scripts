import re
import fnmatch
import os
import sys

if(len(sys.argv) != 3):
	print "You did not enter 2 paramaters. This function requires 2 paramaters to be entered"
	print "Usage: autoIndentCode.py filename_to_be_read filename_to_write_to"
	sys.exit()

try:
	fo = open(sys.argv[1], "r")
except:
	print "The filename " + sys.argv[1] + " could not be opened. Check the name and path and try again."
	sys.exit()

try:
	file_for_writing = open(sys.argv[2], "w")
except:
	print "The filename " + sys.argv[2] + " could not be opened. Check the name and path and try again."
	sys.exit()


def getNumberOfTabs(num_of_tabs):
	mytabs = ""
	for index in range (num_of_tabs):
		mytabs += "	"
	return mytabs

def returnArrayOfIndexPostions(whole_string, specific_char):
    return [i for i, this_letter_of_string in enumerate(whole_string) if this_letter_of_string == specific_char]

tabs_right_now = 0
next_tabs = 0


for line in fo:
	tabs_right_now = next_tabs
	newline = re.sub("^\s+", "", line)
	newline = newline.replace("\n","")
	count_increment = 0
	count_decrement = 0
	if("{" in line):
		count_increment = newline.count("{")
	if("}" in line):
		count_decrement = newline.count("}")

	decrement_indexes = returnArrayOfIndexPostions(newline, "}")
	increment_indexes = returnArrayOfIndexPostions(newline, "{")
	decrement_indexes.sort()
	increment_indexes.sort()

	decrements_that_count = count_decrement
	for each_decrement_index in decrement_indexes:
		lowest_decrement = each_decrement_index
		for each_increment_index in increment_indexes:
			lowest_increment = each_increment_index
			if(lowest_increment < lowest_decrement):
				decrements_that_count -= 1
				increment_indexes.remove(lowest_increment)
				break;

	old_tabs_right_now = tabs_right_now
	tabs_right_now = old_tabs_right_now - decrements_that_count
	next_tabs = old_tabs_right_now + count_increment - count_decrement

	newline = re.sub("^", getNumberOfTabs(tabs_right_now), newline)
	file_for_writing.write(newline+"\n")
