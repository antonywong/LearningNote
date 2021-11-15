using WebApp.Dal;

namespace WebApp.Biz.StockAnalysis
{
    public class BizAPI
    {
        public List<List<String>> GetStocks()
        {
            using (MsSQLDbContext mssql = new MsSQLDbContext())
            {
                List<List<String>> result = mssql.VOption03.OrderBy(x => x.topic).ThenBy(x => x.code).Select(x => new List<String>() { x.code, x.name }).ToList();
                return result;
            }
        }

        public ModelK GetK(String code, Int32 period)
        {
            using (MsSQLDbContext mssql = new MsSQLDbContext())
            {
                ModelK model = new ModelK();
                model.K = mssql.StockK
                    .Where(x => x.code == code && x.type == EnumPeriod.日.GetHashCode())
                    .OrderBy(x => x.day)
                    .Select(x => new List<String>()
                    {
                        x.day.ToString("yyyy-MM-dd"),
                        x.open.ToString("F3"),
                        x.close.ToString("F3"),
                        x.low.ToString("F3"),
                        x.high.ToString("F3")
                    })
                    .ToList();

                model.Strokes = mssql.Stroke
                    .Where(x => x.code == code && x.type == period)
                    .OrderBy(x => x.day)
                    .Select(x => new List<String>()
                    {
                        x.day.ToString("yyyy-MM-dd"),
                        x.extre.ToString("F3")
                    })
                    .ToList();

                return model;
            }
        }
    }
}
