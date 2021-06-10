using System;

namespace WebApp.Dal.SQLite
{
    public class Stock
    {
        public string code { get; set; }
        public Int64 oldHighDays { get; set; }
        public Int64 newHighDays { get; set; }
        public Int64 oldLowDays { get; set; }
        public Int64 newLowDays { get; set; }
        public DateTime updateDate { get; set; }
    }
}