namespace WebApp.Dal.MsSQL
{
    public class VStock01 : BaseStock
    {
        public Nullable<DateTime> lastK05Time { get; set; }
        public Nullable<DateTime> lastKDDate { get; set; }
        public Nullable<DateTime> lastKWDate { get; set; }
        public Nullable<DateTime> lastKMDate { get; set; }
    }
}