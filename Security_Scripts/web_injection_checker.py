import sys
import urllib
import urllib2
import requests
import urlparse

def initialiseSettings():
    my_dict = {}
    settings_file = open("settings.ini", "r")
    for line in settings_file:
        split_line = line.split("=")
        my_dict[split_line[0]] = split_line[1].strip()
    return my_dict

def resultOfSendRequest(s, full_url, cookies, values):
    req = s.post(full_url, values, cookies=cookies)
    return req.text

def testResult(textIfVulnerable, printSuccess, printFail, full_body,myUniqueText):
    if textIfVulnerable in full_body:
        print(printFail)
    else:
        print(printSuccess)
    for line in full_body.splitlines():
        if myUniqueText in line:
            print "For the above result, the line with my text was rendered as: " + line


settings = initialiseSettings()
s = requests.session()
username = settings["username"]
password = settings["password"]
form_val = "Y"
values = { 'login': username,'password': password, 'form': form_val}
cookies = dict(security_level='2')

#need to login before testing real URL
resultOfSendRequest(s,"http://localhost/bWAPP/login.php",cookies,values)

base_url = "http://localhost/bWAPP/htmli_get.php?firstname=A&lastname="
attack_url = "<h2>TTTEST<h2>"
end_of_url = "&form=submit"

#test real URL
full_url = base_url + attack_url + end_of_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM BASIC HTML TAG INJECTION", "VULNERABLE TO BASIC HTML TAG INJECTION", web_result, "TTTEST")

full_url = base_url + urllib.quote_plus(urllib.quote_plus(attack_url)) + end_of_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM ENCODED HTML TAG INJECTION", "VULNERABLE TO ENCODED HTML TAG INJECTION", web_result, "TTTEST")
