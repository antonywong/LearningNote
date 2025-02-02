var http = require('http');
const { exec } = require('child_process');

var server = http.createServer(function(req, res) {
    var msg = exec;
    exec('pm2 start /home/wangyuanjie/v2ray.sh'
      , (error, stdout, stderr) => {
      //   if (error) {
      //     msg = `error: ${error}`;
      //   }
        msg = `stdout: ${stdout}`;
      //   if (stderr) {
      //     msg = `stderr: ${stderr}`;
      //   }
      }
    );
    
    exec('pm2 start /home/wangyuanjie/cloudflared.sh', (error, stdout, stderr) => {});

    msg = 'over!';
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(msg);
});
server.listen(3000);