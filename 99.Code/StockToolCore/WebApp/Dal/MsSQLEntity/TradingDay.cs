using System;

namespace WebApp.Dal.MsSQL
{
    public class TradingDay
    {
        public DateTime date { get; set; }
        public Nullable<Double> balance { get; set; }
    }
}