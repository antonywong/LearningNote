using CH.Common;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace APP
{
    public class Startup
    {
        static Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        public static void Configure(EnumOutputPipeline outputPipeline)
        {
            //配置输出管道
            OutputHelper.Configure(outputPipeline);

            //配置Log4Net
            Log4netHelper.Configure();
            OutputHelper.Write("Log4net配置完成！\r\n");

            OutputHelper.Write("================================================\r\n");




            socket.Bind(new IPEndPoint(IPAddress.Any, 5060));

            socket.Listen(100);

            //接收客户端的 Socket请求   第一个参数是一个委托，第二个参数是第一个参数的参数
            socket.BeginAccept(OnAccept, socket);


        }

        public static void OnAccept(IAsyncResult ar)
        {
            Console.WriteLine("");
            Console.WriteLine(DateTime.Now);
            var serverSocket = ar.AsyncState as Socket;

            //客户端socket
            var clientSocket = serverSocket.EndAccept(ar);

            //服务端进行下一步监听
            serverSocket.BeginAccept(OnAccept, serverSocket);


            var bytes = new byte[1000];
            //获取客户端socket内容
            var len = clientSocket.Receive(bytes);
            //转化正字符串
            var request = Encoding.UTF8.GetString(bytes, 0, len);


            var response = string.Empty;

            //if (!string.IsNullOrEmpty(request) && !request.Contains("favicon.ico"))
            //{
            //    // /1.html
            //    var filePath = request.Split("\r\n")[0].Split(" ")[1].TrimStart('/');

            //    //获取文件内容
            //    response = System.IO.File.ReadAllText(filePath, Encoding.UTF8);
            //}

            Console.WriteLine(request);
            Console.WriteLine("");

            //按照http的响应报文返回
            var responseHeader = string.Format(@"SIP/2.0 401 Unauthorized
Via: SIP/2.0/TCP 10.10.10.133:38421;rport=62843;received=10.10.10.17;branch=z9hG4bK1373306904
From: <sip:34020000001320000001@3402000000>;tag=392973614..To: <sip:34020000001320000001@3402000000>;tag=497633664
CSeq: 1 REGISTER..Call-ID: 1646269925
User-Agent: LiveGBS v210521
Contact: <sip:34020000001320000001@10.10.10.133:5060>
Content-Length: 0
WWW-Authenticate: Digest realm='3402000000',qop='auth',nonce='8b6a222416aada6b135b1909f965077a'");

            //返回给客户端了 可以多次返回
            clientSocket.Send(Encoding.UTF8.GetBytes(responseHeader));
            clientSocket.Send(Encoding.UTF8.GetBytes(response));

            clientSocket.Close();

        }
    }
}
