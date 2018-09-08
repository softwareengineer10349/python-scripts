using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;
using Shorten_URI_App.Models;
using System;

namespace Shorten_URI_App.Controllers
{
    [Route("api/[controller]")]
    public class shortenURIcontroller : ControllerBase
    {
        private readonly shortenURIcontext _context;
        private static char starting_ASCII_char = '0'; 
        private static string starting_ASCII_string = starting_ASCII_char.ToString();
        private static int starting_ASCII_int = (int)starting_ASCII_char;
        private static char ending_ASCII_char = 'z';
        private static int ending_ASCII_int = (int)ending_ASCII_char;
        private static int max_token_length = 7;
        private static int token_length_start_warning = 4; //start logging messages that we're starting to fill up the base URI space when the length of the token is this value

        public shortenURIcontroller(shortenURIcontext context)
        {
            _context = context; //DB Context for Entity Framework

        }

        //Note the Console.WriteLines would really be logged to environment-specific text file, or some other system depending on how you do it, but for simplicity just writes to console
        //I would also put check contraints on the base URI + token being unique, and put an index on (base URI, token) and on long URI for search performance

        //only call when Count > 0
        public ActionResult get_DB_Value_For_Long_URI(string longURI, int statusCode, IEnumerable<URIrecord> already_matching_long_URI){
                 if (already_matching_long_URI.Count() > 1){
                     //Something went very wrong because that shouldn't happen
                     Console.WriteLine("Somehow multiple records were created for longURI: " + longURI + " which are in the database. That shouldn't have happened, please investigate.");
                 }
                 //return already generated short URI
                 var first_already_matching_long_urI = already_matching_long_URI.First(); 
                 return StatusCode(statusCode, first_already_matching_long_urI.baseURI + "/" + first_already_matching_long_urI.token);
        }

public Uri get_real_uri(string longURI){
    string decoded_URI;
        try{
         decoded_URI = Uri.UnescapeDataString(longURI);
        } 
        catch (Exception e){
            Console.WriteLine("Could not decode URI: " + longURI);
            throw new Exception("We couldn't decode the URI (" + longURI + ") for some reason. Please check that you have entered it correctly.");
        }
        Uri uri;
        try{
        uri = new Uri(decoded_URI);
        } catch(Exception e){
            Console.WriteLine("Could not parse URI - as sent to API: " + longURI + ", as decoded by us: " + decoded_URI);
            throw new Exception("We couldn't parse this URI (" + decoded_URI + ") for some reason. Please check that you have entered it correctly.");
        }    
        return uri;
}


        [HttpGet("getEmployee/{URI}/{type}")]
        public ActionResult GetEmployeeWhoGeneratedURI(string getEmployee, string URI, string type){
            if(type != "long" && type != "short"){
                Console.WriteLine("Bad value entered for type in GetEmployeeWhoGeneratedURI, value was: " + type + ", should be either 'short' or 'long'");
                return StatusCode(400, "Please specify either 'short' or 'long' for type");
            }

            Uri uri;
        try{
            uri = get_real_uri(URI);
        } catch(Exception e){
            Console.WriteLine("Errored on trying to decode URI, error: " + e); //e has my custom errors with the URI value it had a problem with
            return StatusCode(400, e);
        }

        IEnumerable<URIrecord> already_matching_URI;
        if(type == "short")
        {
            already_matching_URI = _context.URIrecords.ToList().Where(x => x.baseURI + "/" + x.token == uri.ToString()); //for short URI
        }
        else{
             already_matching_URI = _context.URIrecords.ToList().Where(x => x.longURI == uri.ToString()); //for long URI
        }
                    if(already_matching_URI.Count() > 0){
                        if(already_matching_URI.Count() > 1){
                            Console.WriteLine("Multiple matches were found for the " + type + " URI: " + uri.ToString() + ". That shouldn't have happened, please investigate.");
                        }
                        return StatusCode(200, already_matching_URI.First().employeeID); //just returning the employeeID, really you'd want to join that to an internal DB table to get a whole lot of values but you get the idea
                    }
                    //else
                    return StatusCode(400, "There is no record with the " + type + " URI: " + uri.ToString());

        }

    //[HttpPost]
    [HttpGet("{longURI}/{employeeID}")]
    //public ActionResult Post([FromBody]PostInput myInput)
    //POST requests just didn't want to work with React even though I could make it work with Postman and I just gave up
    public ActionResult Get(string longURI, string employeeID)
    {   
        //string longURI = myInput.longURI;
        //string employeeID = myInput.employeeID;

        if(longURI == null){
            return StatusCode(400, "You need to populate the longURI");
        }

        if(employeeID == null){
            return StatusCode(400, "You need to populate the employeeID");
        }
        
        Uri uri;
        try{
            uri = get_real_uri(longURI);
        } catch(Exception e){
            Console.WriteLine("Errored on trying to decode URI, error: " + e);
            return StatusCode(400, e);
        }

         var already_matching_long_URI = _context.URIrecords.ToList().Where(x => x.longURI == uri.ToString());
             if(already_matching_long_URI.Count() > 0){
                return get_DB_Value_For_Long_URI(longURI, 200, already_matching_long_URI);
             }

        //if here then it doesn't already exist, so create it

        string base_URI = uri.Scheme + "://" + uri.Authority;
        var already_matching_base_URI = _context.URIrecords.ToList().Where(x => x.baseURI == base_URI);
        var new_token = starting_ASCII_string; //this is the start of the characters allowed, which is 0 - 9, a-z, A-Z. 0 goes first because it's first in ASCII.
        if(already_matching_base_URI.Count() > 0){
            //need the next token in sequence
            already_matching_base_URI.OrderBy(x => x.token.Length).ThenBy(x => x.token,StringComparer.Ordinal);
            var lastToken = already_matching_base_URI.Last().token;
            if(lastToken.Length > max_token_length){
                Console.WriteLine("The base URI: "+base_URI+" has a token with over " + max_token_length + " characters, that shouldn't have happened. Please investigate.");
                return StatusCode(400, "We couldn't add the URI " + longURI + " because there is no room to store any more short URI's under " + base_URI + ".");
            }
            if(lastToken == new String(ending_ASCII_char, ending_ASCII_int)){
                Console.WriteLine("The base URI: "+base_URI+" has no more space and somebody tried to make another short URI. You might want to do something about that.");
                return StatusCode(400, "We couldn't add the URI " + longURI + " because there is no room to store any more short URI's under " + base_URI + ".");
            }

            //test if this token is all zzzz so we just need to go up in length
            
            if(lastToken == new String(ending_ASCII_char,  lastToken.Length)){
                new_token = new String(starting_ASCII_char,  lastToken.Length + 1);
                if(lastToken.Length >= token_length_start_warning){ //starting to really fill up, time to start giving people warnings every time we go up a character
                    Console.WriteLine("The base URI: " + base_URI + " just went from " + lastToken.Length + " characters long to " + lastToken.Length + 1 + ", you might want to keep an eye on that");
                }
            }
            else{

                //you also might want to build an interface to release URI tokens, and then store them in some table e.g. ReleasedTokens with the Base URI and token
                //and then if the base URI of this matches anything in that use one of those tokens, remove it from that table and add it to the other table
                //but you get the idea

                //ASCII codes
                //ASCII 48 = character '0'
                //charachters 58 - 64 are not going to be used
                //ASCII 65 is A
                //then it goes until ASCII 90 which is Z
                //then it has some characters we don't want like [
                //then at ASCII 97 we get 'a'
                //finishing at ASCII 122 which is 'z'

                
                for(int i=lastToken.Length - 1; i >= 0; i--){
                    char this_char = lastToken[i];
                    int ASCII = (int)this_char;
                    int startingASCII = ASCII;
                    if(ASCII == 57){
                        ASCII = 65; 
                    }
                    else if(ASCII == 90){
                        ASCII = 97; //we want to skip a few ASCII characters in the sequence so it's just alphanumeric
                    }
                    else if(ASCII < ending_ASCII_int){
                        ASCII++;
                    }
                    if(startingASCII < ending_ASCII_int){
                    char next_increment = (char)ASCII;
                    new_token = "";
                    if(i > 0){
                        new_token += lastToken.Substring(0,i);
                    }
                    new_token += next_increment;
                    if(i < lastToken.Length - 1){
                        new_token += new String(starting_ASCII_char,  lastToken.Length - 1 - i);
                    }
                    break;
                    }
                }
            }
             
        }
        //if no previous records exist, simply create using default specified and output
        _context.URIrecords.Add(new URIrecord {longURI = uri.ToString(), baseURI = base_URI, token = new_token, employeeID = employeeID});
        _context.SaveChanges();

        //Status Code 201: Shortened URI created
        already_matching_long_URI = _context.URIrecords.ToList().Where(x => x.longURI == uri.ToString());
             if(already_matching_long_URI.Count() > 0){
                return get_DB_Value_For_Long_URI(longURI, 201, already_matching_long_URI);
             }
             else{
                 Console.WriteLine("Problem adding URI " + longURI + " that wasn't expected. The system should've created a value for it but it couldn't seem to find it.");
                 return StatusCode(400, "We couldn't add the URI " + longURI + " for some reason. Please contact support for more information.");
             }

        }

    }

    
}