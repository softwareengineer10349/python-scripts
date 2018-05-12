using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using MySql.Data;
using MySql.Data.MySqlClient;
using System.Data;

namespace Dot_Net_Interface.Controllers
{

    public enum JSON_seperator_values {quotes, counts_value}; 
    public enum starting_JSON_headings {names, count, skill_description_amount_of_jobs};
    public enum columns_in_query_to_read {one_first, two_second_first};

    public class callToDB{

        public string connectionString {get; set;}

        public callToDB(){
            string[] lines = System.IO.File.ReadAllLines(@"settings.ini");
            connectionString = "";
            connectionString += lines[0] + ";";
            connectionString += lines[1] + ";";
            connectionString += lines[2] + ";";
            connectionString += lines[3] + ";";
        }

        public MySqlDataReader callStoredProc(string storedProcName, Dictionary<string,string> myParamaters){
            MySql.Data.MySqlClient.MySqlConnection conn = openConnection();
            MySqlCommand cmd = new MySqlCommand(storedProcName, conn);
            cmd.CommandType = CommandType.StoredProcedure;
            foreach (var paramater_name in myParamaters)
            {
              cmd.Parameters.AddWithValue(parameterName: paramater_name.Key, value: paramater_name.Value);  
            }
            MySqlDataReader rdr;
            rdr = cmd.ExecuteReader();
            return rdr;
        }

         public MySql.Data.MySqlClient.MySqlConnection openConnection(){
            MySql.Data.MySqlClient.MySqlConnection conn;
            string myConnectionString = connectionString;
            conn = new MySql.Data.MySqlClient.MySqlConnection();
            conn.ConnectionString = myConnectionString;
            conn.Open();
            return conn;
        }

    }

    public class InfoToCallGoogleCharts{

        public static string[] JSON_GoogleCharts_seperators_for_counts_and_value = new string[]{"{\"c\":[{\"v\":\"", "\",\"f\":null},{\"v\":", ",\"f\":null}]}"};
        public static string[] quotes_seperator = new string[]{"\"", "\""}; 

        public static string ending_JSON = "]}";

        public static string JSON_names_start = "{\"names\":[";
        public static string JSON_count_start = "{\"count\":[";
        public static string JSON_headings_skill_description_amount_of_jobs = "{ \"cols\": [ {\"id\":\"\",\"label\":\"Skill decription\",\"pattern\":\"\",\"type\":\"string\"},  {\"id\":\"\",\"label\":\"Amount of jobs\",\"pattern\":\"\",\"type\":\"number\"}\"rows\": [";

        public static int[] one_index_grab_first = new int[]{0};
        public static int[] two_indexes_grab_second_first = new int[]{1,0};

        public string headings { get; set; }
        public  Dictionary<string, string> dictForGetInfo = new Dictionary<string,string>();
        public string storedProcName { get; set; }
        public string endings = ending_JSON;
        public int[] indexes_of_proc { get; set; }
       
       public string[] list_of_values_between_results {get; set;} 

         public string readValuesFromStoredProc(MySqlDataReader rdr, string[] values_between_results, int[] indexes_of_proc, string headings, string endings){
            string toReturn = headings;
            string delimiter = "";
            while (rdr.Read())
            {
                toReturn += delimiter;
                for (int i=0; i < indexes_of_proc.Length; i++)
                {
                    toReturn += values_between_results[i];
                    toReturn += rdr[i];
                    delimiter = ",";
                }
                toReturn += values_between_results[indexes_of_proc.Length];
                
            }
            rdr.Close();
        
            return toReturn + endings;

        }

        public InfoToCallGoogleCharts(string storedProcInput, columns_in_query_to_read indexGrab, starting_JSON_headings headingType, JSON_seperator_values seperatorType, Dictionary<string,string> mySpecifiedDictionary = null){
            storedProcName = storedProcInput;
            switch (indexGrab)
                {
                    case columns_in_query_to_read.one_first:
                        indexes_of_proc = one_index_grab_first;
                        break;
                    case columns_in_query_to_read.two_second_first:
                        indexes_of_proc = two_indexes_grab_second_first;
                        break;
                    default:
                        throw new Exception("You have used an argument for indexGrab that I have not built a case for");
                }
            switch (headingType)
                {
                    case starting_JSON_headings.names:
                        headings = JSON_names_start;
                        break;
                    case starting_JSON_headings.count:
                        headings = JSON_count_start;
                        break;
                    case starting_JSON_headings.skill_description_amount_of_jobs:
                        headings = JSON_headings_skill_description_amount_of_jobs;
                        break;
                    default:
                        throw new Exception("You have used an argument for headingType that I have not built a case for");
                }
                switch (seperatorType)
                {
                    case JSON_seperator_values.quotes:
                        list_of_values_between_results = quotes_seperator;
                        break;
                    case JSON_seperator_values.counts_value:
                        list_of_values_between_results = JSON_GoogleCharts_seperators_for_counts_and_value;
                        break;
                    default:
                        throw new Exception("You have used an argument for seperatorType that I have not built a case for");
                }

                if(mySpecifiedDictionary != null){
                    dictForGetInfo = mySpecifiedDictionary;
                }
        }

        public string callProc(){
            var myDBconnection = new callToDB();
            var stored_proc = myDBconnection.callStoredProc(storedProcName, dictForGetInfo);
            return readValuesFromStoredProc(stored_proc, list_of_values_between_results,indexes_of_proc, headings, endings);
        }
    }


    [Route("/My_API")]
    public class ValuesController : Controller
    {
        [HttpGet("AllCities")]
        public string GetAllCities()
        {
            var myInfo =  new InfoToCallGoogleCharts("sp_get_all_cities", columns_in_query_to_read.one_first, starting_JSON_headings.names, JSON_seperator_values.quotes);
            return myInfo.callProc();
        }

        [HttpGet("AllJobs/{city}/{skill_type}/{max_results}")]
        public string GetAllJobs(string city, string skill_type, string max_results)
        {
            Dictionary<string, string> dictForGetInfo = new Dictionary<string,string>();
            dictForGetInfo["city_in"] = city;
            dictForGetInfo["skill_type"] = skill_type;
            dictForGetInfo["number_to_display"] = max_results;
            var myInfo =  new InfoToCallGoogleCharts("sp_get_count_of_all_jobs", columns_in_query_to_read.two_second_first, starting_JSON_headings.skill_description_amount_of_jobs, JSON_seperator_values.counts_value, dictForGetInfo);
            return myInfo.callProc();
        }

        [HttpGet("JobNumbers/{city}/{skill_type}/{max_results}/{skill}")]
        public string GetAllJobs(string city, string skill_type, string max_results, string skill)
        {
            Dictionary<string, string> dictForGetInfo = new Dictionary<string,string>();
            dictForGetInfo["city_in"] = city;
            dictForGetInfo["skill_type_in"] = skill_type;
            dictForGetInfo["max_records"] = max_results;
            dictForGetInfo["job_skill_in"] = skill;
            var myInfo =  new InfoToCallGoogleCharts("sp_get_count_of_all_skills_in_city_corresponding_job_skill", columns_in_query_to_read.two_second_first, starting_JSON_headings.skill_description_amount_of_jobs, JSON_seperator_values.counts_value, dictForGetInfo);
            return myInfo.callProc();
        }

        [HttpGet("AllSkills")]
        public string GetAllSkills()
        {
            var myInfo =  new InfoToCallGoogleCharts("sp_get_all_skills", columns_in_query_to_read.one_first, starting_JSON_headings.names, JSON_seperator_values.quotes);
            return myInfo.callProc();
        }

        [HttpGet("AllTypesSkills/{selected_type_in}")]
        public string GetAllTypesSkills(string selected_type_in)
        {
            Dictionary<string, string> dictForGetInfo = new Dictionary<string,string>();
            dictForGetInfo["selected_type"] = selected_type_in;
            var myInfo =  new InfoToCallGoogleCharts("sp_skill_types_not_selected", columns_in_query_to_read.one_first, starting_JSON_headings.names, JSON_seperator_values.quotes, dictForGetInfo);
            return myInfo.callProc();
        }

        [HttpGet("CountAllJobsCity/{job_skill}/{city}")]
        public string CountAllJobsCity(string job_skill, string city)
        {
            Dictionary<string, string> dictForGetInfo = new Dictionary<string,string>();
            dictForGetInfo["job_skill_in"] = job_skill;
            dictForGetInfo["city_in"] = city;
            var myInfo =  new InfoToCallGoogleCharts("sp_get_count_of_all_jobs_in_city", columns_in_query_to_read.one_first, starting_JSON_headings.count, JSON_seperator_values.quotes, dictForGetInfo);
            return myInfo.callProc();
        }
        

    }
}