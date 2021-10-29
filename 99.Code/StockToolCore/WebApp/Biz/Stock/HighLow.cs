using System;
using System.Collections.Generic;
using System.Linq;
using WebApp.Dal;
using WebApp.Dal.MsSQL;

namespace WebApp.Biz.Stock
{
    public class HighLow
    {
        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public static void Run()
        {
            using (MsSQLDbContext mssql = new MsSQLDbContext())
            {
                List<VStock01> stocks = mssql.VStock01.ToList();
                foreach (VStock01 s in stocks)
                {
                    syn(mssql, s);
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public static void Run(MsSQLDbContext mssql, String code)
        {
            List<VStock01> stocks = mssql.VStock01.Where(x => x.code == code).ToList();
            if (stocks.Count > 0)
            {
                syn(mssql, stocks[0]);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        private static void syn(MsSQLDbContext mssql, VStock01 vStock)
        {
            if (vStock.updateDate >= vStock.lastKDDate)
            {
                return;
            }

            List<StockK> days = mssql.StockK.Where(x => x.code == vStock.code && x.type == EnumPeriod.日.GetHashCode()).OrderBy(x => x.day).ToList();
            Int32 newHigh = getHigh(days);
            Int32 newLow = getLow(days);

            Int32 oldHigh = 1;
            Int32 oldLow = 1;
            if (days.Count > 1)
            {
                days.RemoveAt(days.Count - 1);
                oldHigh = getHigh(days);
                oldLow = getLow(days);
            }

            Dal.MsSQL.Stock stock = mssql.Stock.First(x => x.code == vStock.code);
            stock.oldHighDays = oldHigh;
            stock.newHighDays = newHigh;
            stock.oldLowDays = oldLow;
            stock.newLowDays = newLow;
            stock.updateDate = vStock.lastKDDate;
            mssql.Stock.Update(stock);

            mssql.SaveChanges();
            Console.WriteLine($"计算高低值 {vStock.code}--{oldHigh}--{newHigh}--{oldLow}--{newLow}");
        }

        private static Int32 getHigh(List<StockK> days)
        {
            Int32 highDays = 1;
            Double todayHigh = days.Last().high;
            for (int i = 1; i < days.Count; i++)
            {
                Double h = days[days.Count - 1 - i].high;
                if (todayHigh < h)
                {
                    return highDays;
                }
                else
                {
                    highDays++;
                }
            }
            return highDays;
        }

        private static Int32 getLow(List<StockK> days)
        {
            Int32 lowDays = 1;
            Double todayLow = days.Last().low;
            for (int i = 1; i < days.Count; i++)
            {
                Double l = days[days.Count - 1 - i].low;
                if (l < todayLow)
                {
                    return lowDays;
                }
                else
                {
                    lowDays++;
                }
            }
            return lowDays;
        }
    }
}
