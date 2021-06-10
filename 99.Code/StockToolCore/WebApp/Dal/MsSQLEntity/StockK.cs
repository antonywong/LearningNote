using System;

namespace WebApp.Dal.MsSQL
{
    public class StockK
    {
        public String code { get; set; }
        public DateTime day { get; set; }
        public Int32 type { get; set; }
        public Double open { get; set; }
        public Double high { get; set; }
        public Double low { get; set; }
        public Double close { get; set; }
        public Int64 volume { get; set; }
    }
}