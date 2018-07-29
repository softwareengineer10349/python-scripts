import sys
import urllib
import urllib2
import requests
import urlparse
#from bs4 import BeautifulSoup
#from selenium import webdriver
#from seleniumrequests import Firefox
from requestium import Session, Keys
#import re
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import time

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

testsPassed = 0
testsFailed = 0

def testResult(textIfVulnerable, printSuccess, printFail, full_body,myUniqueText):
    global testsFailed
    global testsPassed
    #print full_body
    if textIfVulnerable in full_body:
        print(printFail)
        testsFailed+=1
    else:
        print(printSuccess)
        testsPassed+=1
    for line in full_body.splitlines():
        if myUniqueText in line:
            print "For the above result, the line with my text was rendered as: " + line

def printThisHeading(heading):
    print("\n=========== Running tests for: " + heading +" ===========")


settings = initialiseSettings()
s = requests.session()
username = settings["username"]
password = settings["password"]
form_val = "Y"
values = { 'login': username,'password': password, 'form': form_val}
cookies = dict(security_level='1')

#need to login before testing real URL
resultOfSendRequest(s,"http://localhost/bWAPP/login.php",cookies,values)

base_url = "http://localhost/bWAPP/htmli_get.php?firstname=A&lastname="
attack_url = "<h2>TTTEST<h2>"
end_of_url = "&form=submit"

printThisHeading("GET HTML injection tests")
#test GET URL
full_url = base_url + attack_url + end_of_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM BASIC HTML TAG INJECTION", "VULNERABLE TO BASIC HTML TAG INJECTION", web_result, "TTTEST")

full_url = base_url + urllib.quote_plus(urllib.quote_plus(attack_url)) + end_of_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM ENCODED HTML TAG INJECTION", "VULNERABLE TO ENCODED HTML TAG INJECTION, YOU SHOULD USE FUNCTION htmlspecialchars", web_result, "TTTEST")

printThisHeading("POST HTML injection tests")
#test POST url
base_url = "http://localhost/bWAPP/htmli_post.php"
values = { 'form': form_val, 'firstname' : 'A', 'lastname' : attack_url}
full_url = base_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM BASIC HTML TAG INJECTION", "VULNERABLE TO BASIC HTML TAG INJECTION", web_result, "TTTEST")

values = { 'form': form_val, 'firstname' : 'A', 'lastname' : urllib.quote_plus(attack_url)}
full_url = base_url
web_result = resultOfSendRequest(s,full_url,cookies,values)
testResult("<h2>TTTEST", "SAFE FROM ENCODED HTML TAG INJECTION", "VULNERABLE TO ENCODED HTML TAG INJECTION, YOU SHOULD USE FUNCTION htmlspecialchars", web_result, "TTTEST")

#URL injection
base_url = "http://localhost/bWAPP/htmli_current_url.php"
full_url = base_url + "#" + attack_url
response = s.get(full_url)
testResult("<h2>TTTEST", "SAFE FROM URL INJECTION", "VULNERABLE TO URL INJECTION", response.text, base_url)

#iFrame injection
base_url = "http://localhost/bWAPP/iframei.php"
full_url = base_url + "?ParamUrl=javascript:document.body.innerHTML=%27<h2>TTTEST</h2>%27=works%27&ParamWidth=250&ParamHeight=250"
response = s.get(full_url)
testResult("<h2>TTTEST", "SAFE FROM JAVASCRIPT INJECTION", "VULNERABLE TO JAVASCRIPT INJECTION", response.text, "iframe fr")


print("\n================ Totals =================")
print("Total tests passed: "+str(testsPassed))
print("Total test failed: "+str(testsFailed))
