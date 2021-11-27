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

        /// <summary>
        /// 
        /// </summary>
        /// <param name="now"></param>
        public static void Analyze()
        {
            MsSQLDbContext mssql = new MsSQLDbContext();

            List<String> codes = mssql.Stock.Where(x => x.plate != "ETF").Select(x => x.code).ToList();
            IQueryable<Dal.MsSQL.StockK> kQuery = mssql.StockK.Where(x => x.type == EnumPeriod.日.GetHashCode());
            foreach (String code in codes)
            {
                List<Dal.MsSQL.StockK> ks = kQuery.Where(x => x.code == code)
                    .OrderByDescending(x => x.day)
                    .ToList();
                AnalyzeMA(mssql, ks);
            }

            Dal.MsSQL.TradingDay? lastDay = mssql.TradingDay
                .Where(x => x.mk.HasValue)
                .OrderByDescending(x => x.date)
                .FirstOrDefault();

            IQueryable<Dal.MsSQL.TradingDay> td = mssql.TradingDay.AsQueryable();
            if (lastDay != null)
            {
                td = td.Where(x => x.date > lastDay.date);
            }

            List<Dal.MsSQL.TradingDay> newDays = td.OrderBy(x => x.date).ToList();
            foreach (Dal.MsSQL.TradingDay newDay in newDays)
            {
                if (!AnalyzeOneDay(mssql, newDay, kQuery))
                {
                    break;
                }
            }
        }

        private static void AnalyzeMA(MsSQLDbContext mssql, List<Dal.MsSQL.StockK> ks)
        {
            Boolean needUpdate = false;
            for (Int32 i = 0; i < ks.Count; i++)
            {
                Dal.MsSQL.StockK k = ks[i];
                if (k.ma005.HasValue) { break; }

                List<Dal.MsSQL.StockK> subKs = ks.Skip(i).ToList();
                k.ma005 = AnalyzeMAValue(subKs, 5);
                k.ma010 = AnalyzeMAValue(subKs, 10);
                k.ma020 = AnalyzeMAValue(subKs, 20);
                k.ma030 = AnalyzeMAValue(subKs, 30);
                k.ma060 = AnalyzeMAValue(subKs, 60);
                k.ma250 = AnalyzeMAValue(subKs, 250);
                mssql.StockK.Update(k);
                needUpdate = true;
            }

            if (needUpdate)
            {
                mssql.SaveChanges();
            }
        }

        private static Double? AnalyzeMAValue(List<Dal.MsSQL.StockK> ks, Int32 period)
        {
            if (ks.Count < period)
            {
                return null;
            }
            else
            {
                return ks.Take(period).Select(x => x.close).Average();
            }
        }

        private static Boolean AnalyzeOneDay(MsSQLDbContext mssql, Dal.MsSQL.TradingDay newDay, IQueryable<Dal.MsSQL.StockK> kQuery)
        {
            Console.Write($"横向样本统计：{newDay.date}-");
            List<String> codes = mssql.Stock.Where(x => x.plate != "ETF").Select(x => x.code).ToList();
            List<Dal.MsSQL.StockK> ks = kQuery.Where(x => x.day == newDay.date && codes.Contains(x.code)).ToList();
            if (ks.Count < codes.Count*0.9)
            {
                return false;
            }

            #region 短线上攻
            List<Boolean> sk = new List<Boolean>();
            foreach (Dal.MsSQL.StockK k in ks)
            {
                Int32 skDays = 21;
                List<Dal.MsSQL.StockK> k21 = kQuery.Where(x => x.day <= newDay.date && x.code == k.code)
                    .OrderByDescending(x => x.day)
                    .Take(skDays)
                    .ToList();

                if (k21.Count < skDays) { continue; }

                Double min = k21.Select(x => x.low).Min();
                Double max = k21.Select(x => x.high).Max();

                sk.Add(k21.Last().low <= min && k21.First().high >= max);
            }
            if (sk.Count() > 0) newDay.sk = Convert.ToDouble(sk.Count(x => x)) / Convert.ToDouble(sk.Count());
            Console.Write($"短线上攻-{newDay.sk}-");
            #endregion

            #region 中线上攻
            List<Boolean> mk = new List<Boolean>();
            foreach (Dal.MsSQL.StockK k in ks)
            {
                Boolean ismk = true;

                if (!k.ma005.HasValue) { continue; }
                if (!k.ma010.HasValue) { continue; }
                ismk = ismk && k.ma005.Value >= k.ma010.Value;

                if (!k.ma020.HasValue) { continue; }
                ismk = ismk && k.ma010.Value >= k.ma020.Value;

                if (!k.ma030.HasValue) { continue; }
                ismk = ismk && k.ma020.Value >= k.ma030.Value;

                if (!k.ma060.HasValue) { continue; }
                ismk = ismk && k.ma030.Value >= k.ma060.Value;

                if (!k.ma250.HasValue) { mk.Add(ismk); continue; }
                ismk = ismk && k.ma060.Value >= k.ma250.Value;

                mk.Add(ismk);
            }
            if (mk.Count() > 0) newDay.mk = Convert.ToDouble(mk.Count(x => x)) / Convert.ToDouble(mk.Count());
            Console.WriteLine($"中线上攻-{newDay.mk}");
            #endregion

            mssql.TradingDay.Update(newDay);
            mssql.SaveChanges();

            return true;
        }
    }
}