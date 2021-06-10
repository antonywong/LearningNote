using System;

namespace CH.Common
{
    /// <summary>
    /// 
    /// </summary>
    public enum EnumOutputPipeline
    {
        /// <summary>
        /// 
        /// </summary>
        控制台 = 1,
        /// <summary>
        /// 
        /// </summary>
        日志 = 2
    }

    /// <summary>
    /// 
    /// </summary>
    public class OutputHelper
    {
        private static EnumOutputPipeline _pipeline;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="pipeline"></param>
        public static void Configure(EnumOutputPipeline pipeline)
        {
            _pipeline = pipeline;
        }

        /// <summary>
        /// 
        /// </summary>
        public static void Write(String value)
        {
            switch (_pipeline)
            {
                case EnumOutputPipeline.控制台:
                    Console.WriteLine(value);
                    break;
                case EnumOutputPipeline.日志:
                    Log4netHelper.Logger.Info(value);
                    break;
            }
        }
    }
}
