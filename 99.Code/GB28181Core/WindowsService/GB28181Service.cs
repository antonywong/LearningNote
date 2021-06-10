using APP;
using CH.Common;
using Topshelf;

namespace WindowsService
{
    public class GB28181Service : ServiceControl
    {
        public bool Start(HostControl hostControl)
        {
            EnumOutputPipeline pipe = EnumOutputPipeline.日志;
#if DEBUG
            pipe = EnumOutputPipeline.控制台;
#endif
            Startup.Configure(pipe);
            return true;
        }

        public bool Stop(HostControl hostControl)
        {
            return true;
        }
    }
}
