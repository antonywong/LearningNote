# 端口转发

## 安装
sudo apt install rinetd

## 配置
sudo nano /etc/rinetd.conf
```
命令格式是
bindaddress     bindport        connectaddress      connectport
绑定的地址       绑定的端口       连接的地址           连接的端口
或
[Source Address] [Source Port] [Destination Address] [Destination Port]
源地址            源端口        目的地址               目的端口

0.0.0.0 80 192.168.0.101 80
```

## 运行
pkill rinetd
rinetd -c /etc/rinetd.conf