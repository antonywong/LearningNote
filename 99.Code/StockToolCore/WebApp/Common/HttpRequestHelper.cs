using System;
using System.IO;
using System.Net;
using System.Text;

namespace WebApp.Common
{
    /// <summary>
    /// 
    /// </summary>
    public static class HttpRequestHelper
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        public static String GET(String url)
        {
            return GET(url, Encoding.UTF8);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        public static String GET(String url, Encoding encoding)
        {
            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(url);
            req.Method = "GET";
            HttpWebResponse res = (HttpWebResponse)req.GetResponse();
            StreamReader sr = new StreamReader(res.GetResponseStream(), encoding);
            return sr.ReadToEnd();
        }
    }
}
