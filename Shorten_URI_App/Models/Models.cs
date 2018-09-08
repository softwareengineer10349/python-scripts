using System.ComponentModel.DataAnnotations;

namespace Shorten_URI_App.Models
{
    public class URIrecord
    {
        public string baseURI { get; set; }
        public string token {get; set; }

        [Key]
        public string longURI { get; set; } //key set to longURI because it will be a single unique value

        public string employeeID {get; set; } //for the tracking the CTO wanted
    }

    public class PostInput
    {
        public string longURI {get; set;} 
        public string employeeID {get; set;}
    }
}