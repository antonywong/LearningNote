using System;
using System.Collections.Generic;
using System.Linq;

namespace WebApp.Biz
{
    /// <summary>
    /// 2<=x<=y<=100
    /// S知道x+y，P知道x*y
    /// S：“你不知道xy是多少，我也不知道”
    /// P：“我现在知道了”
    /// S：“我也知道了”
    /// </summary>
    public class Question1
    {
        /// <summary>
        /// 2到200间的素数
        /// </summary>
        private List<Int32> primes = new List<Int32> {
            2,3,5,7,11,13,17,19,23,29,
            31,37,41,43,47,53,59,61,67,71,
            73,79,83,89,97,101,103,107,109,113,
            127,131,137,139,149,151,157,163,167,173,
            179,181,191,193,197,199 };

        private List<Int32> possibleSums = new List<Int32>();

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public void Run()
        {
            List<Int32> oddComposites = new List<Int32>();
            for (Int32 n = 3; n <= 199; n += 2)
            {
                if (!primes.Contains(n))
                {
                    oddComposites.Add(n);
                }
            }
            String strOC = String.Join(',', oddComposites.Select(x => x.ToString()));
            Console.WriteLine($"2到200之间，是奇数且是合数的集合：{strOC}。共{oddComposites.Count}个。\r\n");

            possibleSums = oddComposites.Select(x => x + 2).ToList();
            String strS = String.Join(',', possibleSums.Select(x => x.ToString()));
            Console.WriteLine($"S有可能拿到的数是：{strS}。共{possibleSums.Count}个。\r\n");
            Dictionary<Int32, Object> result = possibleSums.ToDictionary(x => x, x => AnalyzeSum(x));
        }

        private Object AnalyzeSum(Int32 sum)
        {
            Console.WriteLine($"如果S拿到的数是：{sum}。");

            Dictionary<List<Int32>, Object> xys = new Dictionary<List<Int32>, Object>();
            for (Int32 i = 2; i <= sum / 2; i++)
            {
                Int32 x = i;
                Int32 y = sum - i;
                if (x > 100 || y > 100) { continue; }
                Int32 p = x * y;
                Tuple<List<List<Int32>>, Int32> r = AnalyzeProduct(p);

                String sx = x.ToString().PadLeft(3, ' ');
                String sy = y.ToString().PadLeft(3, ' ');
                String sp = p.ToString().PadLeft(4, ' ');
                if (r.Item2 == 1) { Console.ForegroundColor = ConsoleColor.Red; }
                Console.WriteLine($"\t{sum}={sx}+{sy}; {sx}*{sy}={sp}; {r.Item2}个奇合数");
                if (r.Item2 == 1) { Console.ForegroundColor = ConsoleColor.White; }

                xys.Add(new List<Int32>() { x, y }, r);
            }

            return xys;
        }

        private Tuple<List<List<Int32>>, Int32> AnalyzeProduct(Int32 product)
        {
            List<List<Int32>> factors = new List<List<Int32>>();
            Int32 possibleSumCount = 0;
            for (Int32 i = 2; i <= Convert.ToInt32(Math.Sqrt(product)); i++)
            {
                if (product % i == 0)
                {
                    Int32 x = i;
                    Int32 y = product / i;
                    if (x > 100 || y > 100) { continue; }
                    Int32 s = x + y;
                    if (possibleSums.Contains(s)) { possibleSumCount++; }
                    List<Int32> xy = new List<Int32>() { x, y, x + y };

                    String sx = x.ToString().PadLeft(3, ' ');
                    String sy = y.ToString().PadLeft(3, ' ');
                    String ss = s.ToString().PadLeft(3, ' ');
                    //Console.WriteLine($"\t\t{product}={sx}*{sy}; {sx}+{sy}={ss}");

                    factors.Add(xy);
                }
            }

            return new Tuple<List<List<Int32>>, Int32>(factors, possibleSumCount);
        }
    }
}
