namespace WebApp.Dal.MsSQL
{
    public class MyStock
    {
        public string code { get; set; }
        public Int64 fk_accountid { get; set; }
        public String topic { get; set; }
        public Int32 weight { get; set; }
        public Int32 quantity { get; set; }
        public String stagem { get; set; }
        public String stagew { get; set; }
        public String staged { get; set; }
    }
}