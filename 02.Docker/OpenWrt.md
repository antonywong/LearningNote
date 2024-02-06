## 开启网卡的混杂模式
ip link
sudo ip link set eth0 promisc on 

## 创建docker网络
sudo docker network create -d macvlan --subnet=10.10.10.0/23 --gateway=10.10.10.1 -o parent=eth0 macnet
sudo docker network ls

## 镜像
sudo docker pull registry.cn-shanghai.aliyuncs.com/suling/openwrt:x86_64

sudo docker run -d --name openwrt --network macnet \
    --restart=always \
    --privileged registry.cn-shanghai.aliyuncs.com/suling/openwrt:x86_64 /sbin/init

## 配置
sudo docker exec -it openwrt bash

vim /etc/config/network
'''
config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option ipaddr '192.168.2.9'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option gateway '192.168.2.2'
        option broadcast '192.168.2.255'
        option dns '61.177.7.1'
'''
/etc/init.d/network restart

用户名：root
密码：password

## 删除
sudo docker rm openwrt -f


