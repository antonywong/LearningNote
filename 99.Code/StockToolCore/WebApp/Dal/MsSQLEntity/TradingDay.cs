namespace WebApp.Dal.MsSQL
{
    public class TradingDay
    {
        public DateTime date { get; set; }
        public Nullable<Double> profit { get; set; }
        public Nullable<Double> sk { get; set; }
        public Nullable<Double> mk { get; set; }
    }
}