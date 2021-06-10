using System;

namespace WebApp.Dal.MsSQL
{
    public class Stroke
    {
        public String code { get; set; }
        public DateTime day { get; set; }
        public Int32 type { get; set; }
        public Double extre { get; set; }
    }
}