using System;
using System.IO;
using System.Net;
using System.Text;

namespace CH.Common
{
    /// <summary>
    /// 
    /// </summary>
    public static class HttpRequestHelper
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="req"></param>
        /// <returns></returns>
        private static String Send(HttpWebRequest req)
        {
            HttpWebResponse res = (HttpWebResponse)req.GetResponse();
            StreamReader sr = new StreamReader(res.GetResponseStream(), Encoding.UTF8);
            return sr.ReadToEnd();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="method"></param>
        /// <returns></returns>
        private static String Send(String url, String method)
        {
            HttpWebRequest req = GenerateRequest(url, method);
            return Send(req);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="method"></param>
        /// <param name="contentType"></param>
        /// <param name="byteArray"></param>
        /// <returns></returns>
        private static String Send(String url, String method, String contentType, Byte[] byteArray)
        {
            HttpWebRequest req = GenerateRequest(url, method);
            req.ContentType = contentType;
            req.ContentLength = byteArray.Length;
            using (Stream reqStream = req.GetRequestStream())
            {
                reqStream.Write(byteArray, 0, byteArray.Length);
            }

            return Send(req);
        }

        private static HttpWebRequest GenerateRequest(String url, String method)
        {
            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(url);
            req.Method = method;
            req.Host = url.Split("://")[1].Split('/')[0];
            req.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56";
            req.Accept = "*/*";
            return req;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        public static String GET(String url)
        {
            return Send(url, "GET");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="contentType"></param>
        /// <param name="byteArray"></param>
        /// <returns></returns>
        public static String POST(String url, String contentType, Byte[] byteArray)
        {
            return Send(url, "POST", contentType, byteArray);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="json"></param>
        /// <returns></returns>
        public static String PUT(String url, String contentType, Byte[] byteArray)
        {
            return Send(url, "PUT", contentType, byteArray);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="json"></param>
        /// <returns></returns>
        public static String POST_JSON(String url, String json)
        {
            return Send(url, "POST", "application/json", Encoding.UTF8.GetBytes(json));
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="json"></param>
        /// <returns></returns>
        public static String PUT_JSON(String url, String json)
        {
            return Send(url, "PUT", "application/json", Encoding.UTF8.GetBytes(json));
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="url"></param>
        /// <param name="json"></param>
        /// <returns></returns>
        public static String DELETE_JSON(String url, String json)
        {
            return Send(url, "DELETE", "application/json", Encoding.UTF8.GetBytes(json));
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sourceFileURL"></param>
        /// <param name="targetFileFullName"></param>
        /// <returns></returns>
        public static void Download(String sourceFileURL, String targetFileFullName)
        {
            FileInfo fi = new FileInfo(targetFileFullName);
            if (!Directory.Exists(fi.DirectoryName))
            {
                Directory.CreateDirectory(fi.DirectoryName);
            }

            using (FileStream fs = new FileStream(targetFileFullName, FileMode.Create))
            {
                HttpWebRequest req = (HttpWebRequest)WebRequest.Create(sourceFileURL);
                HttpWebResponse res = (HttpWebResponse)req.GetResponse();
                Stream responseStream = res.GetResponseStream();

                //创建本地文件写入流
                byte[] bArr = new byte[1024];
                int size = responseStream.Read(bArr, 0, (int)bArr.Length);
                while (size > 0)
                {
                    fs.Write(bArr, 0, size);
                    size = responseStream.Read(bArr, 0, (int)bArr.Length);
                }
                fs.Close();
                responseStream.Close();
            }
        }
    }
}
