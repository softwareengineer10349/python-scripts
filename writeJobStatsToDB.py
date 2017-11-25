#!/usr/bin/python

import MySQLdb
import os
import glob

#If you need to make a new MySQL user use this:
#CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'new_password';
#GRANT ALL ON Jobs.* TO 'new_user'@'localhost'

general_folder_for_output = "Files_generated_by_script"
username_password_file = open("username password file.txt", "r")
for line in username_password_file:
    username_password_combined = line.split(",")
    username = username_password_combined[0]
    password = username_password_combined[1].strip()
db = MySQLdb.connect("localhost",username,password,"Jobs" )

cursor = db.cursor()

sql_to_create_master = "CREATE TABLE IF NOT EXISTS `master_table` (job_skill VARCHAR(255), PRIMARY KEY(job_skill))"
cursor.execute(sql_to_create_master)

sql_to_create_job_table = "CREATE TABLE IF NOT EXISTS `job_table` (url VARCHAR(255), city VARCHAR(255), job_skill VARCHAR(255), PRIMARY KEY(url,city,job_skill))"
cursor.execute(sql_to_create_job_table)

for each_files in glob.glob(general_folder_for_output + "/*" ):
    if ("lobal" not in each_files and "Run" not in each_files and "Error" not in each_files):
        file_string = each_files.replace("/all_urls_matching_keyword_","").replace(".txt","").replace(general_folder_for_output, "").replace("(","").replace(")","").replace("^"," not ").replace("#"," sharp").replace(" ","_").replace("-","_").strip()
        array_to_split_city = file_string.split("_",1)
        city_of_job = array_to_split_city[0]
        name_of_skill = array_to_split_city[1]
        try:
            sql = "INSERT INTO `master_table` (`job_skill`) VALUES (" + "'" + name_of_skill + "')"
            cursor.execute(sql)
            print "Ran SQL:" sql + "\n"
        except:
            print "Did not run SQL: " + sql + "\n"
        file_to_read = open(each_files, "r")
        for each_line in file_to_read:
            try:
                sql = """INSERT INTO """ + "`job_table` (`url`,`city`,`job_skill`) VALUES('""" + each_line.strip() + """','""" + city_of_job +  """','""" + name_of_skill + """')"""
                cursor.execute(sql)
                print "Ran SQL:" sql+ "\n"
            except:
                print "Did not run SQL: " + sql + "\n"
db.commit()
db.close()
