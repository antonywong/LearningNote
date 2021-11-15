using WebApp.Common;
using WebApp.Dal;
using WebApp.Dal.MsSQL;

namespace WebApp.Biz.Stock
{
    public static class Monitor
    {
        public static Boolean IsRunning = false;
        private static DateTime _now;
        private static EnumPeriod _period;

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public static void Run(DateTime now, EnumPeriod period, String code = "")
        {
            if (IsRunning) { return; }
            IsRunning = true;
            try
            {
                _now = now;
                _period = period;
                using (MsSQLDbContext mssql = new MsSQLDbContext())
                {
                    IQueryable<Dal.MsSQL.Stock> stockQuery = mssql.Stock.Where(x => true);
                    if (_period == EnumPeriod.五分钟 || _period == EnumPeriod.三十分钟)
                    {
                        IQueryable<String> myStockQuery = mssql.MyStock.Select(x => x.code);
                        IQueryable<StockK> deleteKs = mssql.StockK
                            .Where(x => !myStockQuery.Contains(x.code) && x.type == _period.GetHashCode());
                        mssql.StockK.RemoveRange(deleteKs);
                        mssql.SaveChanges();

                        stockQuery = stockQuery.Where(x => myStockQuery.Contains(x.code));
                    }

                    if (!String.IsNullOrWhiteSpace(code))
                    {
                        stockQuery = stockQuery.Where(x => x.code == code);
                    }

                    List<Dal.MsSQL.Stock> stocks = stockQuery.ToList();
                    foreach (Dal.MsSQL.Stock s in stocks)
                    {
                        Int32 result = getStockK(mssql, s);
                        if (result != 0)
                        {
                            Thread.Sleep(1500);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex.Message);
            }
            IsRunning = false;
        }

        public static Int32 getStockK(MsSQLDbContext mssql, Dal.MsSQL.Stock stock)
        {
            Console.Write($"爬虫获取{_period}线{stock.code}：");
            List<StockK> oldK = mssql.StockK.Where(x => x.code == stock.code && x.type == _period.GetHashCode()).OrderByDescending(x => x.day).Take(1).ToList();
            if (oldK.Count > 0)
            {
                switch (_period)
                {
                    case EnumPeriod.五分钟:
                    case EnumPeriod.三十分钟:
                        if (TradingDay.IsTradingDay(_now))
                        {
                            if ((_now - oldK[0].day).TotalMinutes < _period.GetHashCode() || oldK[0].day.Date == _now.Date.AddHours(15))
                            {
                                return 0;
                            }
                        }
                        else
                        {
                            if (oldK[0].day.Date == TradingDay.PreviousTradingDay(_now).AddHours(15))
                            {
                                return 0;
                            }
                        }
                        break;
                    case EnumPeriod.日:
                        if (TradingDay.IsTradingDay(_now))
                        {
                            if (_now.Date == oldK[0].day || (TradingDay.PreviousTradingDay(_now) == oldK[0].day && (_now.Hour * 100 + _now.Minute) < 1530))
                            {
                                return 0;
                            }
                        }
                        else
                        {
                            if (TradingDay.PreviousTradingDay(_now) == oldK[0].day)
                            {
                                return 0;
                            }
                        }
                        break;
                    case EnumPeriod.周:
                        if (_now.DayOfWeek != DayOfWeek.Saturday && _now.DayOfWeek != DayOfWeek.Sunday || (_now - oldK[0].day).TotalDays < 7)
                        {
                            return 0;
                        }
                        break;
                    case EnumPeriod.月:
                        if ((oldK[0].day.Year * 100 + oldK[0].day.Month) >= (_now.Year * 100 + _now.Month))
                        {
                            return 0;
                        }
                        break;
                    default:
                        throw new NotImplementedException();
                }
            }

            Int32 datalen = Math.Min(500, Convert.ToInt32(360000 / _period.GetHashCode()));
            var url = $"http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={stock.code}&scale={_period.GetHashCode()}&datalen={datalen}";
            String res = HttpRequestHelper.GET(url);
            List<SinaK> resKs = JsonHelper.FromJson<List<SinaK>>(res);
            if (oldK.Count == 0)
            {
                resKs.RemoveAt(resKs.Count - 1);
            }
            else
            {
                resKs = resKs.Where(x => DateTime.Parse(x.day) > oldK[0].day).ToList();
            }

            if (resKs.Count > 0)
            {
                List<StockK> ks = mssql.StockK
                    .Where(x => x.code == stock.code && x.type == _period.GetHashCode())
                    .OrderByDescending(x => x.day)
                    .Skip(datalen)
                    .Take(1)
                    .ToList();
                if (ks.Count > 0)
                {
                    mssql.StockK.RemoveRange(mssql.StockK.Where(x => x.code == stock.code && x.type == _period.GetHashCode() && x.day <= ks[0].day));
                }

                mssql.StockK.AddRange(resKs.Select(x => new StockK()
                {
                    code = stock.code,
                    day = DateTime.Parse(x.day),
                    type = _period.GetHashCode(),
                    open = Convert.ToDouble(x.open),
                    high = Convert.ToDouble(x.high),
                    low = Convert.ToDouble(x.low),
                    close = Convert.ToDouble(x.close),
                    volume = Int64.Parse(x.volume)
                }));
                mssql.SaveChanges();
            }

            Console.WriteLine($"{resKs.Count}条数据");
            return resKs.Count;
        }
    }
}
