import re
import fnmatch
import os
import sys
import copy

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

def removeIndexesBetween(array_quotes_outer, array_quotes_inner, first_index_outer, first_index_inner, actual_inner_array):
	print "outer_quote_array = "+str(array_quotes_outer)
	print "inner_quote_array = "+str(array_quotes_inner)
	outer_quote_end = array_quotes_outer[1]
	array_quotes_outer.remove(first_index_outer)
	array_quotes_outer.remove(outer_quote_end)
	for each_inner_index in array_quotes_inner:
		if(each_inner_index < outer_quote_end):
			actual_inner_array.remove(each_inner_index)
			array_quotes_inner.remove(each_inner_index)
		else:
			break

def removeQuotesIfQuoted(array_of_single_quotes, array_of_double_quotes,final_index):
	if(len(array_of_single_quotes) > 0 and len(array_of_double_quotes) > 0):
		copy_array_single = copy.copy(array_of_single_quotes)
		copy_array_double = copy.copy(array_of_double_quotes)
		if(len(copy_array_single) > len(copy_array_double)):
			copy_array_double.append(final_index)
		if(len(copy_array_double) > len(copy_array_single)):
			copy_array_single.append(final_index)
		while(len(copy_array_double) > 0 and len(copy_array_single) > 0):
			first_index_double = copy_array_double[0]
			first_index_single = copy_array_single[0]
			if first_index_single < first_index_double:
				removeIndexesBetween(copy_array_single, copy_array_double, first_index_single, first_index_double, array_of_double_quotes)
			else:
				removeIndexesBetween(copy_array_double, copy_array_single, first_index_double, first_index_single, array_of_single_quotes)

def sortArrays(list_of_Arrays):
	for each_array in list_of_Arrays:
		each_array.sort()

def valueOfQuoteOn(array_of_quotes, quote_on, added_index):
	return (len(array_of_quotes) + quote_on - added_index) % 2

def compensateIfQuoteOn(quote_on, quote_indexes):
		if(quote_on == 1):
			quote_indexes.insert(0,0)
			return 1
		return 0

tabs_right_now, next_tabs, double_quote_on, single_quote_on = 0, 0, 0, 0

for line in fo:
	tabs_right_now = next_tabs
	newline = re.sub("^\s+", "", line)
	print "For the line of code: "+ newline
	newline = newline.replace("\n","")
	count_increment, count_decrement, added_index_single, added_index_double = 0, 0, 0, 0
	last_index_of_line = len(newline)-1

	decrement_indexes = returnArrayOfIndexPostions(newline, "}")
	increment_indexes = returnArrayOfIndexPostions(newline, "{")
	double_quote_indexes = returnArrayOfIndexPostions(newline, "\"")
	single_quote_indexes = returnArrayOfIndexPostions(newline, "\'")
	added_index_double = compensateIfQuoteOn(double_quote_on,double_quote_indexes)
	added_index_single = compensateIfQuoteOn(single_quote_on,single_quote_indexes)
	removeFromArrayIfPreviousIsBackslash(double_quote_indexes, newline)
	removeFromArrayIfPreviousIsBackslash(single_quote_indexes, newline)
	sortArrays([double_quote_indexes,single_quote_indexes])
	removeQuotesIfQuoted(single_quote_indexes, double_quote_indexes,last_index_of_line)
	sortArrays([double_quote_indexes,single_quote_indexes,decrement_indexes, increment_indexes])
	removeFromArrayIfQuoted(increment_indexes,double_quote_indexes,double_quote_on,last_index_of_line)
	removeFromArrayIfQuoted(decrement_indexes,double_quote_indexes,double_quote_on,last_index_of_line)
	removeFromArrayIfQuoted(increment_indexes,single_quote_indexes,single_quote_on,last_index_of_line)
	removeFromArrayIfQuoted(decrement_indexes,single_quote_indexes,single_quote_on,last_index_of_line)
	count_increment = len(increment_indexes)
	count_decrement = len(decrement_indexes)
	sortArrays([decrement_indexes,increment_indexes])
	double_quote_on = valueOfQuoteOn(double_quote_indexes, double_quote_on,added_index_double)
	single_quote_on = valueOfQuoteOn(single_quote_indexes, single_quote_on, added_index_single)

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
