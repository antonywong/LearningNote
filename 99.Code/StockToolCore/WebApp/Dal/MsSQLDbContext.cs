using Microsoft.EntityFrameworkCore;
using WebApp.Dal.MsSQL;

namespace WebApp.Dal
{
    public class MsSQLDbContext : DbContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlServer(@"Data Source=10.10.10.18;Initial Catalog=CH_Stock;User Id=sa;Password=sql@0512;");
        }

        public DbSet<TradingDay> TradingDay { get; set; }

        public DbSet<Stock> Stock { get; set; }
        public DbSet<StockK> StockK { get; set; }
        public DbSet<Stroke> Stroke { get; set; }

        public DbSet<MyStock> MyStock { get; set; }

        public DbSet<VStock01> VStock01 { get; set; }
        public DbSet<VOption03> VOption03 { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<TradingDay>().HasKey(x => new { x.date });

            modelBuilder.Entity<Stock>().HasKey(x => new { x.code });
            modelBuilder.Entity<StockK>().HasKey(x => new { x.code, x.day, x.type });
            modelBuilder.Entity<Stroke>().HasKey(x => new { x.code, x.day, x.type });

            modelBuilder.Entity<MyStock>().HasKey(x => new { x.code });

            modelBuilder.Entity<VStock01>().HasKey(x => new { x.code });
            modelBuilder.Entity<VOption03>().HasKey(x => new { x.code });
        }
    }
}
