using Microsoft.EntityFrameworkCore;

namespace Shorten_URI_App.Models
{
    public class shortenURIcontext : DbContext
    {
        public shortenURIcontext(DbContextOptions<shortenURIcontext> options)
            : base(options)
        {
        }

        public DbSet<URIrecord> URIrecords { get; set; }
    }
}