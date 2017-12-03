#!/usr/bin/env python

import urllib2
import sys
import re
import datetime
import os
import glob

dictionary_of_times = {}

list_of_times = []
list_of_times.append("Start time: "+str(datetime.datetime.now()))

list_of_cities = {"Brisbane" : "in-Brisbane-CBD-&-Inner-Suburbs-Brisbane-QLD",
"Melbourne" :  "in-Melbourne-CBD-&-Inner-Suburbs-Melbourne-VIC",
"Sydney" : "in-Sydney-CBD,-Inner-West-&-Eastern-Suburbs-Sydney-NSW"}
#list_of_cities = {"Brisbane": "in-Brisbane-CBD-&-Inner-Suburbs-Brisbane-QLD"}
dictionary_of_all_dictionary_values = {}
dictionary_of_total_counts = {}
dictionary_of_unmatched = {}
dictionary_of_filehandles = {}
dictionary_of_matched = {}
it_url = "https://www.seek.com.au/jobs-in-information-communication-technology"
pages_to_search = 1000
string_for_job_title = "article aria-label=\"([\s\S]+?)\""
string_for_job_url = "href=\"\/job\/([\s\S]+?)\""
dictionary_of_counts_matched_global = {}

class JobSkill:
     def __init__(self, regex_String, name_String, category):
         self.regex = regex_String
         self.name = name_String
         #string_of_all = category.join("_")
         self.category = '_'.join(category)

list_of_programming_skills = [
 JobSkill("(\\.|dot) ?NET[^/]",".NET",["Language"]),
 JobSkill("SQL", "SQL", ["Language","Databases"]),
JobSkill("database","Database",["Technology","Databases"]),
JobSkill("perl","Perl",["Language","Scripting"]),
JobSkill("python","Python",["Language","Scripting","Web"]),
JobSkill("(ruby on rails|[^A-z]ror[^A-z])","Ruby on rails)",["Language","Web"]),
JobSkill("ruby","Ruby",["Language"]),
JobSkill("java ","Java",["Language"]),
JobSkill("android","Android",["Technology","Mobile"]),
JobSkill("ios","iOS",["Technology","Mobile"]),
JobSkill("C\\+\\+","C++",["Language"]),
JobSkill("C#","C#",["Language"]),
JobSkill("[^A-z]C[^A-z\\+#]","C",["Language"]),
JobSkill("web","Web",["Technology","Web"]),
JobSkill("php","Php",["Language","Web"]),
JobSkill("security", "Security",["Technology","Job Type"]),
JobSkill("angular","Angular",["Framework","Web","Javascript Framework"]),
JobSkill("vue","Vue.js",["Framework","Web","Javascript Framework"]),
JobSkill("jquery","jQuery",["Framework","Web","Javascript Framework"]),
JobSkill("laravel", "Laravel", ["Framework","Web","PHP Framework"]),
JobSkill("sys(tem )?admin", "System administration", ["Job Type"]),
JobSkill("redis","Redis",["Databases","Technology"]),
JobSkill("linux","Linux",["OS","Technology"]),
JobSkill("unix","Unix",["OS","Technology"]),
JobSkill("mobile","Mobile",["Mobile","Technology"]),
JobSkill("network","Network",["Technology"]),
JobSkill("xamarin","Xamarin",["Mobile"]),
JobSkill("analy(st|tic)","Analyst",["Job Type"]),
JobSkill("test","test",["Additional Skill"]),
JobSkill("engineer","Engineer",["Job Type"]),
JobSkill("developer","developer",["Job Type"]),
JobSkill("node","Node.js",["Framework","Web","Javascript Framework"]),
JobSkill("sap[^A-z]","SAP",["Databases"]),
JobSkill("sharepoint","Sharepoint",["Technology"]),
JobSkill("RHEL", "Red Hat Enterprise Linux",["OS","Technology"]),
JobSkill("devops","Devops",["Additional Skills"]),
JobSkill("lead", "Lead", ["Job level"]),
JobSkill("( UX|user experience)","User Experience",["Additional Skills"]),
JobSkill("(manager|supervisor)","Manager",["Job level"]),
JobSkill("HANA", "HANA", ["Databases","Technology"]),
JobSkill("powershell","Powershell",["Technology"]),
JobSkill("drupal","Drupal",["Technology"]),
JobSkill("help ?desk","Help desk",["Job Type"]),
JobSkill("programmer", "Programmer",["Job Type"]),
JobSkill("gam(e|ing)","Gaming",["Job Type"]),
JobSkill("architect","Architect",["Job Type"]),
JobSkill("cloud","Cloud",["Technology"]),
JobSkill("[^A-z]vb[^A-z]","VB",["Language"]),
JobSkill("Windows","Windows",["OS","Company"]),
JobSkill("Red Rat","Red Hat",["Company"]),
JobSkill("React","React",["Web","Framework","Javascript Framework"]),
JobSkill("neo ?4 ?j","Neo4j",["Databases"]),
JobSkill("(JS|Javascript)","Javascript",["Web","Language"]),
JobSkill("azure","Azure",["Technology"]),
JobSkill("wpf","WPF",["Technology","Web"]),
JobSkill("front.?end","Front End",["Job Type"]),
JobSkill("html","HTML",["Web","Language"]),
JobSkill("css","CSS",["Web","Language"]),
JobSkill("redux","Redux",["Technology"]),
JobSkill("(aws|amazon web service)","AWS",["Technology","Web"]),
JobSkill("wordpress","Wordpress",["Technology"]),
JobSkill("full.stack", "Full Stack",["Job Type"]),
JobSkill("swift", "Swift",["Language"]),
JobSkill("senior","Senior",["Job level"]),
JobSkill("junior","Junior",["Job level"]),
JobSkill("pen(etration)? ?test","Penetration tester",["Job Type"]),
JobSkill("mysql", "MySQL",["Web","Databases"]),
JobSkill("oracle","Oracle",["Company","Databases"]),
JobSkill("sql ?server", "SQL Server",["Databases"]),
JobSkill("(go[^A-z]|golang)","Go (language)",["Language"]),
JobSkill("(shell|bash)","Shell",["Technology","Language"]),
JobSkill("scala[^A-z]","Scala",["Language"]),
JobSkill("mongo","MongoDB",["Databases"]),
JobSkill("django","Django",["Web","Framework","Python Framework"]),
JobSkill("kubernetes","Kubernetes",["Technology"]),
JobSkill("docker","Docker",["Technology"]),
JobSkill("flask", "Flask",["Web","Framework","Python Framework"]),
JobSkill("spring","Spring",["Framework","Java Framework"]),
JobSkill("hibernate","Hibernate",["Framework","Java Framework"]),
JobSkill("hadoop","Hadoop",["Databases"]),
JobSkill("postgresql", "PostgreSQL",["Databases"]),
JobSkill("cakephp","CakePHP",["Framework", "PHP Framework"]),
JobSkill("zend", "Zend",["Framework","PHP Framework"]),
JobSkill("symfony","Symfony",["Framework","PHP Framework"])
]


general_folder_for_output = "Files_generated_by_script"

start_filename_for_writing = general_folder_for_output + '/all_urls_matching_keyword_'
filename_for_writing_global_stats = general_folder_for_output + '/_Global.txt'

if not os.path.exists(general_folder_for_output):
    os.makedirs(general_folder_for_output)

for old_files in glob.glob(general_folder_for_output + "/*" ):
    os.remove(old_files)

run_log = open(general_folder_for_output + "/_Run_log.txt", "w")
error_log = open(general_folder_for_output + "/_Error_log.txt", "w")
my_logs = [run_log, error_log]

#for each_keyword in list_of_programming_keywords:
for each_job_skill in list_of_programming_skills:
    each_keyword = each_job_skill.regex
    dictionary_of_counts_matched_global[each_keyword] = 0
    for each_city in list_of_cities:
        my_key = each_city + "_" + each_job_skill.name + "_" + each_job_skill.category# each_keyword.replace(" ","_").replace("\\","").replace(".","dot").replace("+","plus").replace("?","").replace("[","").replace("]","")
        dictionary_of_filehandles[my_key] = open(start_filename_for_writing + my_key + ".txt", 'w')

list_of_city_urls = []

for city_key in list_of_cities:
    list_of_times.append("Started city "+city_key + " : " + str(datetime.datetime.now()))
    city_url = list_of_cities[city_key]
    city_url = it_url + "/" + city_url
    total_count_for_city = 0
    total_matched_for_city = 0
    total_unmatched_for_city = 0
    dictionary_counts_for_this_city = dictionary_of_counts_matched_global.copy()
    attempts_before_killing = 10
    attempt_counter = 0
    for p_number in range(1,pages_to_search):
        run_log.write("for the city " + city_key + ",for the page "+str(p_number) + " at time: " + str(datetime.datetime.now()) + "\n")
        my_url = city_url + "/" + "?page=" + str(p_number)
        #try for each page
        try:
            jobs_found_on_page = 0
            response = urllib2.urlopen(my_url)
            html = response.read()
            html = html.replace("href","\nhref")
            #match_title = re.findall(string_for_job_title,html)
            #for each_match_title in match_title:
                #print "for the matching title "+each_match_title
                #job_title = each_match_title
            match_url = re.findall(string_for_job_url,html)
            match_url = list(set(match_url))
            hit_match=0
            for job_url in match_url:
                #print "for the job url "+job_url
                total_count_for_city += 1
                actual_url = "https://www.seek.com.au/job/"+job_url
                #try for each job url
                try:
                    this_job_response = urllib2.urlopen(actual_url)
                    this_job_html = this_job_response.read()
                    jobs_found_on_page += 1
                    search_for_description_in_box = "class=\"templatetext\"[\s\S]+?<\/div>"
                    description_in_box = re.search(search_for_description_in_box,this_job_html,re.IGNORECASE)
                    job_info = description_in_box.group(0)
                    #for keyword in list_of_programming_keywords:
                    for each_job_skill in list_of_programming_skills:
                        keyword = each_job_skill.regex
                        match_in_job_page = re.search(keyword, job_info, re.IGNORECASE)
                        if(match_in_job_page):
                            dictionary_counts_for_this_city[keyword] += 1
                            hit_match=1
                            keyword_file_safe = city_key + "_" + each_job_skill.name + "_" + each_job_skill.category #keyword.replace(" ","_").replace("\\","").replace(".","dot").replace("+","plus").replace("?","").replace("[","").replace("]","")
                            file_for_writing_urls = dictionary_of_filehandles[keyword_file_safe]
                            file_for_writing_urls.write(actual_url+"\n")
                except:
                    run_log.write("Ignored exception " + str(sys.exc_info()[0]) + " on page "+str(p_number) + " on job URL " + job_url)
        except:
            error_log.write("Couldn't find the page. Exception: " + str(sys.exc_info()[0])+"\n")
            attempt_counter += 1
            if (attempt_counter >= attempts_before_killing):
                error_log.write("Killing because there aren't more pages at "+str(datetime.datetime.now())+"\n")
                break
        if(hit_match == 1):
            total_matched_for_city += 1
        else:
            total_unmatched_for_city += 1
        if(jobs_found_on_page == 0):
            attempt_counter += 1
            if (attempt_counter >= attempts_before_killing):
                error_log.write("Killing because there aren't more pages at "+str(datetime.datetime.now())+"\n")
                break

    dictionary_of_matched[city_key] = total_matched_for_city
    dictionary_of_unmatched[city_key] = total_unmatched_for_city
    dictionary_of_all_dictionary_values[city_key] = dictionary_counts_for_this_city
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

dictionary_1 = dictionary_of_all_dictionary_values[dictionary_of_all_dictionary_values.keys()[0]]

#for every keyword
for key, value in sorted(dictionary_1.iteritems(), key=lambda (k,v): (v,k)):
    string_to_print = "For key: "+key + " - "
    #for every city
    for each_city_key in list_of_cities:
        string_to_print += each_city_key + " value was: "
        #get dictionary of this particular city with that value
        this_dict = dictionary_of_all_dictionary_values[each_city_key]
        string_to_print += str(this_dict[key]) + ", "
    file_for_writing_stats.write(string_to_print+"\n")

list_of_times.append("Finish time : " + str(datetime.datetime.now()))

file_for_writing_stats.write("\n***************************************\nInformation on how long this script took to run:\n")
for each_time in list_of_times:
    file_for_writing_stats.write(each_time + "\n")

file_for_writing_stats.close()
for each_log in my_logs:
    each_log.close()
