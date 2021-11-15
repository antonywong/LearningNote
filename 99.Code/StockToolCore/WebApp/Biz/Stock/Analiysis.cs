using WebApp.Dal;
using WebApp.Dal.MsSQL;

namespace WebApp.Biz.Stock
{
    public static class Analiysis
    {
        public static Boolean IsRunning = false;
        private static EnumPeriod _period;

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public static void Run(EnumPeriod period, String code = "")
        {
            if (IsRunning) { return; }
            IsRunning = true;
            try
            {
                _period = period;
                using (MsSQLDbContext mssql = new MsSQLDbContext())
                {
                    List<Dal.MsSQL.Stock> stocks = String.IsNullOrWhiteSpace(code) ? mssql.Stock.ToList() : mssql.Stock.Where(x => x.code == code).ToList();
                    foreach (Dal.MsSQL.Stock s in stocks)
                    {
                        Analyse(mssql, s);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex.Message);
            }
            IsRunning = false;
        }

        private static void Analyse(MsSQLDbContext mssql, Dal.MsSQL.Stock stock)
        {
            Console.Write($"分析{_period}线{stock.code}  ");
            List<Stroke> strokes = mssql.Stroke
                .Where(x => x.code == stock.code && x.type == _period.GetHashCode())
                .OrderByDescending(x => x.day)
                .Take(2)
                .ToList();

            if (strokes.Count <= 0)
            {
                strokes = InitAnaliysis(mssql, stock);
            }
            Tuple<Stroke, Stroke> stroke = new Tuple<Stroke, Stroke>(strokes[1], strokes[0]);

            List<StockK> ks = mssql.StockK
                .Where(x => x.code == stock.code && x.type == _period.GetHashCode() && x.day >= stroke.Item2.day)
                .OrderBy(x => x.day)
                .ToList();

            while (ks.Count > 1)
            {
                List<StockK> sliceKs = ks.Take(5).ToList();

                Boolean directionUp = stroke.Item1.extre < stroke.Item2.extre;
                if (directionUp)
                {
                    Int32 nextHIndex = Max(sliceKs);
                    if (nextHIndex == 0)//出顶分型
                    {
                        if (sliceKs.Count < 5)//未形成下一笔
                        {
                            break;
                        }
                        else//可形成下一笔
                        {
                            Stroke newStroke = new Stroke();
                            newStroke.code = stock.code;
                            newStroke.day = sliceKs[4].day;
                            newStroke.type = _period.GetHashCode();
                            newStroke.extre = sliceKs[4].low;
                            mssql.Stroke.Add(newStroke);

                            stroke = new Tuple<Stroke, Stroke>(stroke.Item2, newStroke);
                            ks.RemoveRange(0, 4);
                        }
                    }
                    else//上升一笔的延伸
                    {
                        Stroke newStroke = new Stroke();
                        newStroke.code = stock.code;
                        newStroke.day = sliceKs[nextHIndex].day;
                        newStroke.type = _period.GetHashCode();
                        newStroke.extre = sliceKs[nextHIndex].high;
                        mssql.Stroke.Add(newStroke);
                        mssql.Stroke.Remove(stroke.Item2);

                        stroke = new Tuple<Stroke, Stroke>(stroke.Item1, newStroke);
                        ks.RemoveRange(0, nextHIndex);
                    }
                }
                else
                {
                    Int32 nextLIndex = Min(sliceKs);
                    if (nextLIndex == 0)//出底分型
                    {
                        if (sliceKs.Count < 5)//未形成下一笔
                        {
                            break;
                        }
                        else//可形成下一笔
                        {
                            Stroke newStroke = new Stroke();
                            newStroke.code = stock.code;
                            newStroke.day = sliceKs[4].day;
                            newStroke.type = _period.GetHashCode();
                            newStroke.extre = sliceKs[4].high;
                            mssql.Stroke.Add(newStroke);

                            stroke = new Tuple<Stroke, Stroke>(stroke.Item2, newStroke);
                            ks.RemoveRange(0, 4);
                        }
                    }
                    else//下降一笔的延伸
                    {
                        Stroke newStroke = new Stroke();
                        newStroke.code = stock.code;
                        newStroke.day = sliceKs[nextLIndex].day;
                        newStroke.type = _period.GetHashCode();
                        newStroke.extre = sliceKs[nextLIndex].low;
                        mssql.Stroke.Add(newStroke);
                        mssql.Stroke.Remove(stroke.Item2);

                        stroke = new Tuple<Stroke, Stroke>(stroke.Item1, newStroke);
                        ks.RemoveRange(0, nextLIndex);
                    }
                }

                mssql.SaveChanges();
            }
        }

        private static List<Stroke> InitAnaliysis(MsSQLDbContext mssql, Dal.MsSQL.Stock stock)
        {
            List<StockK> ks = mssql.StockK
                .Where(x => x.code == stock.code && x.type == _period.GetHashCode())
                .OrderBy(x => x.day)
                .Take(5)
                .ToList();
            Int32 li = ks.Count - 1;

            List<Stroke> result = new List<Stroke>() {
                new Stroke() { code = stock.code, day = ks[li].day, type = _period.GetHashCode() },
                new Stroke() { code = stock.code, day = ks[0].day, type = _period.GetHashCode() }
            };
            if (ks[0].high < ks[li].high)
            {
                result[0].extre = ks[li].high;
                result[1].extre = ks[0].low;
            }
            else
            {
                result[0].extre = ks[li].low;
                result[1].extre = ks[0].high;
            }

            mssql.Stroke.AddRange(result);
            mssql.SaveChanges();

            return result;
        }

        private static Int32 Max(List<StockK> ks)
        {
            Double maxValue = ks[0].high;
            Int32 maxIndex = 0;
            for (Int32 i = 1; i < ks.Count; i++)
            {
                if (ks[i].high > maxValue)
                {
                    maxValue = ks[i].high;
                    maxIndex = i;
                }
            }
            return maxIndex;
        }

        private static Int32 Min(List<StockK> ks)
        {
            Double minValue = ks[0].low;
            Int32 minIndex = 0;
            for (Int32 i = 1; i < ks.Count; i++)
            {
                if (ks[i].low < minValue)
                {
                    minValue = ks[i].low;
                    minIndex = i;
                }
            }
            return minIndex;
        }
    }
}