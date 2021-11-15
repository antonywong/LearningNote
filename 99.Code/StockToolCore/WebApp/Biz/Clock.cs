using System.Timers;
using WebApp.Biz.Stock;
using Monitor = WebApp.Biz.Stock.Monitor;

namespace WebApp.Biz
{
    /// <summary>
    /// 定时任务
    /// </summary>
    public static class Clock
    {
        /// <summary>
        /// 定时时钟
        /// </summary>
        public static System.Timers.Timer timer = null;

        /// <summary>
        /// 配置并启动定时闹钟程序
        /// </summary>
        public static void Configure()
        {
            //Monitor.Run(DateTime.Now, EnumPeriod.五分钟);

            //Monitor.Run(DateTime.Now, EnumPeriod.日);
            //HighLow.Run();
            //Analiysis.Run(EnumPeriod.日);

            //Monitor.Run(DateTime.Now, EnumPeriod.周);
            //Analiysis.Run(EnumPeriod.周);

            //Monitor.Run(DateTime.Now, EnumPeriod.月);
            //Analiysis.Run(EnumPeriod.月);
            //return;

            TradingDay.Configure();

            Monitor.Run(DateTime.Now, EnumPeriod.五分钟);

            if (TradingDay.IsTradingDay(DateTime.Now))
            {
                StockInfo.Run();
                Monitor.Run(DateTime.Now, EnumPeriod.日);
                HighLow.Run();
            }

            Int64 interval = 60 * 1000;//每分钟

            timer = new System.Timers.Timer();
            timer.Elapsed += new ElapsedEventHandler(Timer_Elapsed);
            timer.Interval = interval;
            timer.AutoReset = true;
            timer.Enabled = true;
        }

        /// <summary>
        /// 计时器触发事件
        /// </summary>
        /// <param name="sender"></param>
        private static void Timer_Elapsed(Object sender, ElapsedEventArgs e)
        {
            timer.Enabled = false;
            try
            {
                DateTime now = DateTime.Now.ToLocalTime();
                Int32 hm = now.Hour * 100 + now.Minute;

                if (TradingDay.IsTradingDay(now))
                {
                    Console.Write(hm.ToString() + ";\r\n");

                    //
                    if (hm == 915) { StockInfo.Run(); }

                    //
                    if ((935 <= hm && hm <= 1132 || 1305 <= hm && hm <= 1502) && !Monitor.IsRunning) { Monitor.Run(now, EnumPeriod.五分钟); }

                    //
                    if (1530 <= hm && hm <= 1545 && !Monitor.IsRunning) { Monitor.Run(now, EnumPeriod.日); HighLow.Run(); }

                    //
                    if (hm == 1700)
                    {
                        Analiysis.Run(EnumPeriod.日);
                    }
                }

                //
                if (now.DayOfWeek == DayOfWeek.Sunday && hm == 200)
                {
                    Monitor.Run(now, EnumPeriod.周);
                    Analiysis.Run(EnumPeriod.周);
                }

                //
                if (now.Day == 1 && hm == 100)
                {
                    Monitor.Run(now, EnumPeriod.月);
                    Analiysis.Run(EnumPeriod.月);
                }
            }
            catch(Exception ex)
            {
                Console.Write(ex.Message);
            }
            timer.Enabled = true;
        }

        /// <summary>
        /// 关闭定时任务闹钟程序
        /// </summary>
        public static void Stop()
        {
            if (timer != null)
            {
                timer.Stop();
            }
        }

        /// <summary>
        /// 销毁
        /// </summary>
        public static void Dispose()
        {
            if (timer != null)
            {
                timer.Close();
                timer.Dispose();
            }
        }
    }
}