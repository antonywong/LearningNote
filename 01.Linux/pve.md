# 设置宿主机(PVE服务器)网络参数

## 开启ipv4、ipv6转发：/etc/sysctl.conf
在文件最后加入如下配置
'''
net.ipv4.ip_forward=1
net.ipv4.conf.all.rp_filter=1
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.conf.default.forwarding=1
net.ipv4.conf.default.proxy_arp = 0
net.ipv4.conf.default.send_redirects = 1
net.ipv4.conf.all.send_redirects = 0
net.ipv6.conf.eno1.autoconf=0
net.ipv6.conf.eno1.accept_ra=2
net.ipv6.conf.default.forwarding=1
net.ipv6.conf.all.forwarding=1
net.ipv6.conf.default.proxy_ndp=1
net.ipv6.conf.all.proxy_ndp=1
'''

## 配置Proxmox VE网卡文件信息：/etc/network/interfaces
'''
auto lo
iface lo inet loopback

iface enp2s0 inet manual

auto vmbr0
iface vmbr0 inet static
    address 10.10.10.18/23
    gateway 10.10.10.1
    bridge-ports enp2s0
    bridge-stp off
    bridge-fd 0

#物理网卡配置一般不做改动，系统模板都是配置好的。
#为虚拟机新建一个虚拟网桥
#内网地址，虚拟机的网关
auto vmbr172          
iface vmbr172 inet static
    address  10.20.30.1/24
    bridge-ports none
    bridge-stp off
    bridge-fd 0
    post-up echo 1 > /proc/sys/net/ipv4/ip_forward
    post-up echo 1 > /proc/sys/net/ipv4/conf/eno1/proxy_arp
    #转发IPv4流量到虚拟机，使虚拟机与外网联通。
    post-up iptables -t nat -A POSTROUTING -s '10.20.30.0/24' -o vmbr0 -j MASQUERADE
    post-down iptables -t nat -D POSTROUTING -s '10.20.30.0/24' -o vmbr0 -j MASQUERADE
'''

## 重启服务
service networking restart

## NAT
### 新增
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 3389 -j DNAT --to-destination 10.20.30.100:3389
### 删除 （即把新增映射的-A改成-D）
iptables -t nat -D PREROUTING -p tcp -m tcp --dport 3389 -j DNAT --to-destination 10.20.30.100:3389
### 查看NAT规则，并显示行号
iptables -t nat --list --line-number
### 删除指定行号的iptables规则
iptables -t nat -D POSTROUTING 10





iptables -t nat -A PREROUTING -p tcp -m tcp --dport 7890 -j DNAT --to-destination 10.20.30.100:7890
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 10808 -j DNAT --to-destination 10.20.30.100:10808

