using Microsoft.EntityFrameworkCore;
using WebApp.Dal.SQLite;

namespace WebApp.Dal
{
    public class SQLiteDbContext : DbContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite(@"Data Source=Z:/StockTool.db");
        }

        public DbSet<Stock> Stock { get; set; }

        public DbSet<StockKD> StockKD { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Stock>().HasKey(x => x.code);
            modelBuilder.Entity<StockKD>().HasKey(x => x.id);
        }
    }
}
