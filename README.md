# python-scripts

This is just a series of python scripts that I have made which might be useful to other people.

========================= autoIndentCode.py =================================

Made for Python 2 and made to be run using the format: python autoIndentCode.py filename_to_be_read filename_to_write_to

autoIndentCode.py is a script I made for a friend who struggles to read code without indenting.

It will read the input filename and convert it to something which is indented based on brackets.
E.g. for a file which had the lines:

code{

here

}

It will convert it to:

code{

	here

}

Feel free to use it if you have access to something that will run Python and want to convert some code into something more readable.
It can also be useful if you're having an issue with brackets to quickly figure out where an extra bracket should or should not go.
You can copy/paste code from something and put it into a file, and then run the script on that. Then look at the file you told it to write to.
It will not alter the file you read from, so you don't have to worry about it overwriting anything.

===================== webCrawler.py =========================================

Made for Python 2 and made to be run using the format: ./webCrawler.py. Don't forget to
make sure the script is executable.

webCrawler.py is a script I made to work out what languages/skills were actually used commercially.
It searches seek.com.au for the locations specified, then searches through every single IT job
description for the keywords I've told it to look for, and then counts how many jobs mention
the keyword.

It can take a while to run so you may want to kick it off and then go do something else.
