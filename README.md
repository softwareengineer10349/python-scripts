# python-scripts

This started as just a series of python scripts that I have made.
I then wanted to use the output from the Python scripts in databases and web so it evolved somewhat.

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

Made for Python 2 and made to be run using the format: ./webCrawler.py.

webCrawler.py is a script I made to work out what languages/skills were actually used commercially.
It searches seek.com.au for the locations specified, then searches through every single IT job
description for the keywords I've told it to look for, and then counts how many jobs mention
the keyword.

It can take a while to run so you may want to kick it off and then go do something else.

I wanted to analyse this data a bit so I wrote a script to put it in a MySQL DB.
You can read about this below.

========================== writeJobStatsToDB.py ===============================

Made for Python 2 and made to be run using to format: ./writeJobStatsToDB.py.

This is a script I made to take the results of webCrawler.py and write it to a DB.
I mostly did this because I wanted to do some inner joins to look at correlations between skills.
Sure, I know that Javascript is the most popular language, but what is the most popular
language for jobs that have Python in it? Or PHP?

I then decided to write a web interface to view the results, so I could make easy to read charts,
 which you can read about below.

========================== Web_interface_Javascript_PHP =======================

The web interface which displays the results from webCrawler.py.

It lets you select what city you want to pull results from, what type of skill you
want to pull results from (e.g. language, framework, etc.), how many results you
want to see and shows you a graph of the most popular skills matching that criteria.
It also lets you select which skill you want to analyse further and then gives you a graph
of the skills which are the most highly correlated to the skill you're interested in.

Server side all in PHP, client side in HTML/CSS/Javascript/jQuery, charts using Google Charts (with Javascript).
