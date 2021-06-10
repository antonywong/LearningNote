using System;
using System.Collections.Generic;
using System.Linq;
using WebApp.Dal;

namespace WebApp.Biz.Stock
{
    /// <summary>
    /// 
    /// </summary>
    public static class TradingDay
    {
        /// <summary>
        /// 
        /// </summary>
        public static void Configure()
        {
            List<DateTime> newDate = new List<DateTime>();
            for (Int32 i = 0; i < 30; i++)
            {
                DateTime current = DateTime.Now.Date.AddDays(i);
                if (current.DayOfWeek != DayOfWeek.Saturday && current.DayOfWeek != DayOfWeek.Sunday)
                {
                    newDate.Add(current);
                }
            }

            MsSQLDbContext mssql = new MsSQLDbContext();
            List<DateTime> dateQuery = mssql.TradingDay
                .OrderByDescending(x => x.date)
                .Take(1)
                .Select(x => x.date)
                .ToList();
            if (dateQuery.Count > 0)
            {
                newDate = newDate.Where(x => x > dateQuery[0]).ToList();
            }

            mssql.TradingDay.AddRange(newDate.Select(x => new Dal.MsSQL.TradingDay()
            {
                date = x
            }));
            mssql.SaveChanges();
        }

        private static DateTime _today = DateTime.MinValue;
        private static Boolean _isTradingDay = false;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="now"></param>
        public static Boolean IsTradingDay(DateTime now)
        {
            if (_today != now.Date)
            {
                _today = now.Date;

                Configure();

                MsSQLDbContext mssql = new MsSQLDbContext();
                _isTradingDay = mssql.TradingDay.Any(x => x.date == _today);
            }
            return _isTradingDay;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="now"></param>
        public static DateTime PreviousTradingDay(DateTime now)
        {
            MsSQLDbContext mssql = new MsSQLDbContext();
            return mssql.TradingDay
                .Where(x => x.date < now.Date)
                .OrderByDescending(x => x.date)
                .FirstOrDefault()
                .date;
        }
    }
}