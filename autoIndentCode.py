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

def removeFromArrayIfPreviousIsBackslash(array_to_test,line_to_test):
	for each_index in array_to_test:
		previous_index = each_index - 1
		if(previous_index >= 0):
			if(line_to_test[previous_index] == "\\"):
				previous_previous_index = previous_index - 1
				if(previous_previous_index >= 0):
					if(line_to_test[previous_previous_index] != "\\"):
						array_to_test.remove(each_index)
				else:
					array_to_test.remove(each_index)

def removeFromArrayIfQuoted(array_of_brackets, array_of_quotes, currently_on, final_index):
	if(currently_on == 1):
		array_of_quotes.insert(0,0)
	start_quote_array = []
	end_quote_array = []
	counter = 0
	for each_quote_index in array_of_quotes:
		if (counter == 0):
			start_quote_array.append(each_quote_index)
			counter = 1
			continue
		if (counter == 1):
			end_quote_array.append(each_quote_index)
			counter = 0
			continue
	if(len(start_quote_array) > len(end_quote_array)):
		end_quote_array.append(final_index)
	for i in range(0, len(start_quote_array)):
		start_index = start_quote_array[i]
		end_index = end_quote_array[i]
		for each_bracket_index in array_of_brackets:
			if(start_index <= each_bracket_index and end_index >= each_bracket_index):
				array_of_brackets.remove(each_bracket_index)

tabs_right_now = 0
next_tabs = 0
double_quote_on = 0
single_quote_on = 0

for line in fo:
	tabs_right_now = next_tabs
	newline = re.sub("^\s+", "", line)
	newline = newline.replace("\n","")
	count_increment = 0
	count_decrement = 0

	decrement_indexes = returnArrayOfIndexPostions(newline, "}")
	increment_indexes = returnArrayOfIndexPostions(newline, "{")
	double_quote_indexes = returnArrayOfIndexPostions(newline, "\"")
	single_quote_indexes = returnArrayOfIndexPostions(newline, "\'")
	removeFromArrayIfPreviousIsBackslash(double_quote_indexes, newline)
	removeFromArrayIfPreviousIsBackslash(single_quote_indexes, newline)
	double_quote_indexes.sort()
	single_quote_indexes.sort()
	decrement_indexes.sort()
	increment_indexes.sort()
	removeFromArrayIfQuoted(increment_indexes,double_quote_indexes,double_quote_on,len(newline)-1)
	removeFromArrayIfQuoted(decrement_indexes,double_quote_indexes,double_quote_on,len(newline)-1)
	removeFromArrayIfQuoted(increment_indexes,single_quote_indexes,single_quote_on,len(newline)-1)
	removeFromArrayIfQuoted(decrement_indexes,single_quote_indexes,single_quote_on,len(newline)-1)
	count_increment = len(increment_indexes)
	count_decrement = len(decrement_indexes)
	decrement_indexes.sort()
	increment_indexes.sort()
	double_quote_on = (len(double_quote_indexes)+double_quote_on) % 2
	single_quote_on = (len(single_quote_indexes)+single_quote_on) % 2

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
