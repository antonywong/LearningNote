using System;

namespace WebApp.Dal.MsSQL
{
    public class BaseStock
    {
        public string code { get; set; }
        public string name { get; set; }
        public Nullable<Int32> oldHighDays { get; set; }
        public Nullable<Int32> newHighDays { get; set; }
        public Nullable<Int32> oldLowDays { get; set; }
        public Nullable<Int32> newLowDays { get; set; }
        public Nullable<DateTime> updateDate { get; set; }
    }
}