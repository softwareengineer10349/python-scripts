import re
import fnmatch
import os

fileExtension=".txt"

for file in os.listdir('.'):
	if fnmatch.fnmatch(file, 'dumbCode.*'):
		new_file_extension=file.split(".")
		if(len(new_file_extension)>0):
			fileExtension=new_file_extension[1]
			break
		

fo = open("dumbCode."+fileExtension, "r") #replace with your filename of the file to read



file_for_writing=open("indented."+fileExtension,"w") #replace with the new filename you want


def getNumberOfTabs(num_of_tabs):
	mytabs = ""
	for index in range (num_of_tabs):
		mytabs += "	"
	return mytabs

tabs_right_now = 0
next_tabs = 0
for line in fo:
	tabs_right_now = next_tabs
	newline = re.sub("^\s+", getNumberOfTabs(tabs_right_now), line)
	count_increment = 0
	count_decrement = 0
	if("{" in line):
		count_increment = line.count("{")
	if("}" in line):
		count_decrement = line.count("}")
	total_change_in_line = count_increment - count_decrement
	decrements_that_count = count_decrement - count_increment
	if(decrements_that_count < 0):
		decrements_that_count = 0
	old_tabs_right_now = tabs_right_now
	tabs_right_now = old_tabs_right_now - decrements_that_count 
	next_tabs = old_tabs_right_now + count_increment - count_decrement 
	newline = re.sub("^", getNumberOfTabs(tabs_right_now), newline)
	file_for_writing.write(newline)