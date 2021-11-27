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
        public Double? ma005 { get; set; }
        public Double? ma010 { get; set; }
        public Double? ma020 { get; set; }
        public Double? ma030 { get; set; }
        public Double? ma060 { get; set; }
        public Double? ma250 { get; set; }
    }
}