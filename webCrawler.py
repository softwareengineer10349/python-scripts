#!/usr/bin/env python

import urllib2
import sys
import re
import datetime
import os
import glob

print "Script started at: " + str(datetime.datetime.now())


list_of_cities = {"Brisbane" : "in-Brisbane-CBD-&-Inner-Suburbs-Brisbane-QLD",
"Melbourne" :  "in-Melbourne-CBD-&-Inner-Suburbs-Melbourne-VIC",
"Sydney" : "in-Sydney-CBD,-Inner-West-&-Eastern-Suburbs-Sydney-NSW"}
#list_of_cities = ["in-Brisbane-CBD-&-Inner-Suburbs-Brisbane-QLD"]
list_of_all_dictionary_values = {}
dictionary_of_total_counts = {}
dictionary_of_unmatched = {}
dictionary_of_filehandles = {}
dictionary_of_matched = {}
it_url = "https://www.seek.com.au/jobs-in-information-communication-technology"
pages_to_search = 2
string_for_job_title = "article aria-label=\"([\s\S]+?)\""
string_for_job_url = "href=\"\/job\/([\s\S]+?)\""
dictionary_of_counts_matched_global = {}
list_of_programming_keywords = ["\\.NET", "SQL", "database", "perl", "python", "ruby on rails",
"ruby", "java ", "android", "ios", "C\\+\\+", "C#", "[^A-z]C[^A-z\\+#]", "perl", "web", "php",
"security", "pentest", "angular", "vue", "jquery", "laravel", "sysadmin", "redis",
"linux", "unix", "mobile", "network", "itsm", "xamarin", "analyst", "test", "engineer",
"developer", "node", "sap", "sharepoint", "RHEL", "devops", "lead", " UX", "manager",
"HANA", "administrator", "operator", "powershell", "drupal", "helpdesk", "help desk", "support",
"programmer", "administration", "installer", "automation", "sales", "game",
"supervisor", "designer", "video", "consultant", "coordinator", "analytic",
"technician", "writer", "architect", "improvement", "cloud", "vb ", "vba ", "vb\\.net",
 "transformation", "telecommunication", "system", "digital", "entry", " IT ", "information",
"Win ", "React", "project", "communication", "cerner", "iam", "service", "neo ?4 ?j",
"resource", "JS", "data", "scientist", "azure", "director", "specialist",
"expression", "concierge", "officer", "partner", "executive", "account",
"technical", "operation", "wpf", "javascript", "front", "html", "css",
"soa", "redux", "aws", "serverless", "wordpress", "bi ", "full", " GIS",
"dot", "swift", "aem", "crm", "j2ee", "sap", "commerce", "senior", "junior",
"mid", "pen test", "mysql", "oracle", "sql ?server", "go[^A-z]", "golang", "shell",
"bash", "scala[^A-z]", "mongo", "django", "kubernetes", "docker", "flask", "ror",
"t-sql", "mvc", "fin ?tech", "spring", "hibernate", "contract", "app ", "hadoop",
"postgresql", "blockchain", "cakephp", "zend", "symfony", "Amazon web"]


general_folder_for_output = "Files_generated_by_script"
start_filename_for_writing = general_folder_for_output + '/all_urls_matching_keyword_'
filename_for_writing_global_stats = general_folder_for_output + '/_Global.txt'

if not os.path.exists(general_folder_for_output):
    os.makedirs(general_folder_for_output)

for old_files in glob.glob(general_folder_for_output + "/*" ):
    os.remove(old_files)

for each_keyword in list_of_programming_keywords:
    dictionary_of_counts_matched_global[each_keyword] = 0
    for each_city in list_of_cities:
        my_key = each_city + "_" + each_keyword.replace(" ","_").replace("\\","").replace(".","dot").replace("+","plus").replace("?","").replace("[","").replace("]","")
        dictionary_of_filehandles[my_key] = open(start_filename_for_writing + my_key + ".txt", 'w')

list_of_city_urls = []

for city_key in list_of_cities:
    city_url = list_of_cities[city_key]
    city_url = it_url + "/" + city_url
    total_count_for_city = 0
    total_matched_for_city = 0
    total_unmatched_for_city = 0
    dictionary_counts_for_this_city = dictionary_of_counts_matched_global.copy()
    attempts_before_killing = 10
    attempt_counter = 0
    for p_number in range(1,pages_to_search):
        print "for the city " + city_key + ",for the page "+str(p_number) + " at time: " + str(datetime.datetime.now())
        my_url = city_url + "/" + "?page=" + str(p_number)
        #try for each page
        try:
            jobs_found_on_page = 0
            response = urllib2.urlopen(my_url)
            html = response.read()
            html = html.replace("href","\nhref")
            match_title = re.findall(string_for_job_title,html)
            #for each_match_title in match_title:
                #print "for the matching title "+each_match_title
                #job_title = each_match_title
            match_url = re.findall(string_for_job_url,html)
            match_url = list(set(match_url))
            hit_match=0
            for job_url in match_url:
                print "for the job url "+job_url
                total_count_for_city += 1
                actual_url = "https://www.seek.com.au/job/"+job_url
                #try for each job url
                try:
                    this_job_response = urllib2.urlopen(actual_url)
                    this_job_html = this_job_response.read()
                    jobs_found_on_page += 1
                    for keyword in list_of_programming_keywords:
                        #print "for the keyword "+keyword
                        #search_for_keyword_in_box = "class=\"templatetext\"[\s\S]+?"+keyword+"[\s\S]+?<\/div>"
                        search_for_description_in_box = "class=\"templatetext\"[\s\S]+?"+"[\s\S]+?<\/div>"
                        #match_in_job_page = re.search(search_for_description_in_box,this_job_html,re.IGNORECASE)
                        description_in_box = re.search(search_for_description_in_box,this_job_html,re.IGNORECASE)
                        job_info = description_in_box.group(0)
                        match_in_job_page = re.search(keyword, job_info, re.IGNORECASE)
                        if(match_in_job_page):
                            dictionary_counts_for_this_city[keyword] += 1
                            hit_match=1
                            keyword_file_safe = city_key + "_" + keyword.replace(" ","_").replace("\\","").replace(".","dot").replace("+","plus").replace("?","").replace("[","").replace("]","")
                            file_for_writing_urls = dictionary_of_filehandles[keyword_file_safe] #open(start_filename_for_writing+keyword_file_safe+".txt", 'a')
                            file_for_writing_urls.write(actual_url+"\n")
                except:
                    print "Ignored exception " + str(sys.exc_info()[0]) + " on page "+str(p_number)

        except:
            print "Couldn't find the page. Exception: " + str(sys.exc_info()[0])
            attempt_counter += 1
            if (attempt_counter >= attempts_before_killing):
                print "Killing because there aren't more pages"
                break
        if(hit_match == 1):
            total_matched_for_city += 1
        else:
            total_unmatched_for_city += 1
        if(jobs_found_on_page == 0):
            attempt_counter += 1
            if (attempt_counter >= attempts_before_killing):
                print "Killing because there aren't more pages"
                break

    dictionary_of_matched[city_key] = total_matched_for_city
    dictionary_of_unmatched[city_key] = total_unmatched_for_city
    list_of_all_dictionary_values[city_key] = dictionary_counts_for_this_city
    dictionary_of_total_counts[city_key] = total_count_for_city


string_to_print_count_matched = "Total count for the matched values for the city "
string_to_print_count_unmatched = "Total count for the unmatched values for the city "
string_to_print_total_jobs = "Total count for the amount of jobs for the city "

for each_count_key in dictionary_of_total_counts:
    string_to_print_count_unmatched += each_count_key + " was: " + str(dictionary_of_unmatched[each_count_key]) + ", "
    string_to_print_total_jobs +=  each_count_key + " was: "+ str(dictionary_of_total_counts[each_count_key]) + ", "
    string_to_print_count_matched += each_count_key + " was: "+ str(dictionary_of_total_counts[each_count_key]) + ", "

for key_filename in dictionary_of_filehandles:
    dictionary_of_filehandles[key_filename].close()

file_for_writing_stats = open(filename_for_writing_global_stats, 'a')
file_for_writing_stats.write(string_to_print_total_jobs+"\n")
file_for_writing_stats.write(string_to_print_count_matched+"\n")
file_for_writing_stats.write(string_to_print_count_unmatched+"\n")

dictionary_1 = list_of_all_dictionary_values["Brisbane"]

#for every keyword
for key, value in sorted(dictionary_1.iteritems(), key=lambda (k,v): (v,k)):
    string_to_print = "For key: "+key + " - "
    #for every city
    for each_city_key in list_of_cities:
        string_to_print += each_city_key + " value was: "
        #get dictionary of this particular city with that value
        this_dict = list_of_all_dictionary_values[each_city_key]
        string_to_print += str(this_dict[key]) + ", "
    file_for_writing_stats.write(string_to_print+"\n")

file_for_writing_stats.close()
