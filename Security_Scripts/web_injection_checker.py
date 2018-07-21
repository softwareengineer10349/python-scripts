import sys
import urllib
import urllib2
import requests

def initialiseSettings():
    my_dict = {}
    settings_file = open("settings.ini", "r")
    for line in settings_file:
        split_line = line.split("=")
        my_dict[split_line[0]] = split_line[1].strip()
    return my_dict

settings = initialiseSettings()

s = requests.session()

username = settings["username"]
password = settings["password"]
form_val = "Y"

#need to login before testing real URL
values = { 'login': username,'password': password, 'form': form_val}
full_url = "http://localhost/bWAPP/login.php"
req = s.post(full_url, values)
the_page = req.text

#test real URL
full_url = "http://localhost/bWAPP/htmli_get.php?firstname=A&lastname=<marquee>TEST<marquee>&form=submit"

cookies = dict(security_level='0')
req = s.post(full_url, values, cookies=cookies)
full_body = req.text

if "marquee&gt;TEST" in full_body:
    #print("BODY = "+full_body)
    print("SAFE FROM BASIC HTML TAG INJECTION")
else:
    #print("BODY = "+full_body)
    print("VULNERABLE TO BASIC HTML TAG INJECTION")
