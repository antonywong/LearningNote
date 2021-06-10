using System;
using Topshelf;

namespace WindowsService
{
    class Program
    {
        static void Main(string[] args)
        {
            HostFactory.Run(x =>
            {
                x.Service<GB28181Service>();
                x.EnableServiceRecovery(r => r.RestartService(TimeSpan.FromSeconds(10)));
                x.SetServiceName("GB28181Core");
                x.SetDisplayName("瀚远文物安全数据采集服务");
                x.SetDescription("瀚远文物安全数据采集服务");
                x.StartAutomatically();
            });
        }
    }
}
