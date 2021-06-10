using log4net;
using log4net.Config;
using System;
using System.IO;

namespace CH.Common
{
    /// <summary>
    /// 
    /// </summary>
    public class Log4netHelper
    {
        private static ILog _logger;

        /// <summary>
        /// 
        /// </summary>
        public static void Configure()
        {
            var repository = LogManager.CreateRepository("NETCoreRepository");
            XmlConfigurator.Configure(repository, new FileInfo(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Configs/log4net.config")));
            _logger = LogManager.GetLogger(repository.Name, "InfoLogger");
        }

        /// <summary>
        /// 
        /// </summary>
        public static ILog Logger { get { return _logger; } }
    }
}
