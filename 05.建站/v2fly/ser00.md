
# 使用pm2进程管理
## 一键安装pm2
bash <(curl -s https://raw.githubusercontent.com/k0baya/alist_repl/main/serv00/install-pm2.sh)

## 创建进程
pm2 start /home/wangyuanjie/v2ray-serv00/v2ray --watch -- run --config=/home/wangyuanjie/v2ray-serv00/config.json
pm2 start /home/wangyuanjie/cloudflared-freebsd --watch -- --config  /home/wangyuanjie/.cloudflared/config.yml tunnel run 45cef9f1-9505-48ce-ae72-04bbea446726

## 脚本
#!/bin/bash

/home/wangyuanjie/v2ray-serv00/v2ray run --config=/home/wangyuanjie/v2ray-serv00/config.json


#!/bin/bash

/home/wangyuanjie/cloudflared-freebsd --config  /home/wangyuanjie/.cloudflared/config.yml tunnel run 45cef9f1-9505-48ce-ae72-04bbea446726
