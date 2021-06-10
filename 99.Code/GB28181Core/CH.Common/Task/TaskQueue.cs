using System;
using System.Collections.Generic;
using System.Threading;

namespace CH.Common
{
    /// <summary>
    /// 任务队列项
    /// </summary>
    public interface ITaskQueueItem
    {
        /// <summary>
        /// 出队列时运行的方法
        /// </summary>
        void Run();
    }

    /// <summary>
    /// 任务队列
    /// 仅支持集成ITaskQueueItem接口的类
    /// </summary>
    public static class TaskQueue
    {
        /// <summary>
        /// 计算任务队列
        /// </summary>
        private static Queue<ITaskQueueItem> _taskQueue { get; set; } = new Queue<ITaskQueueItem>();

        /// <summary>
        /// 计算任务最大线程数
        /// </summary>
        private static int CalThreadMaxNum { get { return 20; } }

        /// <summary>
        /// 获取当前任务队列数量
        /// </summary>
        /// <returns></returns>
        public static Int32 GetQueueNum()
        {
            return _taskQueue.Count;
        }

        /// <summary>
        /// 向计算队列中加入计算任务
        /// </summary>
        /// <param name="task">计算任务</param>
        public static void Push(ITaskQueueItem task)
        {
            lock (_taskQueue)
            {
                _taskQueue.Enqueue(task);
            }
            StartCalculate();
        }

        /// <summary>
        /// 出任务队列
        /// </summary>
        /// <returns>计算任务</returns>
        public static ITaskQueueItem PopTask()
        {
            if (GetQueueNum() == 0)
            {
                return null;
            }
            ITaskQueueItem task;
            lock (_taskQueue)
            {
                task = _taskQueue.Dequeue();
            }
            return task;
        }

        /// <summary>
        /// 开始计算
        /// </summary>
        private static void StartCalculate()
        {
            if (CalThreadNum < CalThreadMaxNum)
            {
                CalculateEntity entity = new CalculateEntity();
                Thread t = new Thread(new ThreadStart(entity.Start));
                t.IsBackground = true;
                CalThreadNum++;
                t.Start();
            }
        }

        /// <summary>
        /// 测试，成功次数
        /// </summary>
        public static Int32 SuccessNum = 0;

        /// <summary>
        /// 运行中的线程数
        /// </summary>
        public static Int32 CalThreadNum = 0;
    }

    /// <summary>
    /// 计算任务控制类
    /// </summary>
    public class CalculateEntity
    {
        /// <summary>
        /// 开始
        /// </summary>
        public void Start()
        {
            //当任务队列大于0时，获取排在最前面的任务执行
            if (TaskQueue.GetQueueNum() > 0)
            {
                string message = string.Empty;
                try
                {
                    ITaskQueueItem task = TaskQueue.PopTask();
                    if (task != null)
                    {
                        DateTime start = DateTime.Now;
                        task.Run();
                        DateTime end = DateTime.Now;
                    }
                }
                catch (Exception ex)
                {
                    Log4netHelper.Logger.Error(String.Format("任务处理异常：{0}\r\n系统异常信息：{1}", message, (ex.Message + "\r\n" + ex.StackTrace)));
                }
            }
            //执行完成
            End();
        }

        /// <summary>
        /// 执行完成
        /// </summary>
        private void End()
        {
            //判断任务队列中是否存在任务，有的话继续，没有的话关闭线程
            if (TaskQueue.GetQueueNum() > 0)
            {
                this.Start();
            }
            TaskQueue.CalThreadNum--;
        }
    }
}
