using System;

namespace WebApp.Dal.SQLite
{

    public class StockKD
    {
        public Int64 id { get; set; }
        public string code { get; set; }
        public DateTime day { get; set; }
        public Double open { get; set; }
        public Double high { get; set; }
        public Double low { get; set; }
        public Double close { get; set; }
        public Int64 volume { get; set; }
        public Nullable<Double> ma5 { get; set; }
        public Nullable<Double> ma10 { get; set; }
    }
}