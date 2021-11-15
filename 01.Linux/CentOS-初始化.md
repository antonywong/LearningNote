# 网络设置

## 修改IP
vi /etc/sysconfig/network-scripts/ifcfg-******
设置：
    bootproto="static"
    onboot="yes"
    IPADDR="10.10.11.230"
    PREFIX="23"
    GATEWAY="10.10.10.1"
    DNS1="61.177.7.1"

# 配置SSH
## 首先，要确保CentOS7安装了  openssh-server
yum list installed | grep openssh-server
yum install openssh-server

## 修改ssh配置文件：
vi /etc/ssh/sshd_config
设置
    Port 22
    ListenAddress 0.0.0.0
    ListenAddress ::

## 启动ssh
systemctl start sshd
systemctl enable sshd

## 检查sshd服务是否已经开启
ps -e | grep sshd


# 防火墙

## 服务
    systemctl start firewalld
    systemctl stop firewalld
    systemctl enable firewalld
    systemctl status firewalld

## 重新加载
    firewall-cmd --state                        Return and print firewalld state
    firewall-cmd --reload                       Reload firewall and keep state information
    firewall-cmd --complete-reload              Reload firewall and lose state information
    firewall-cmd --runtime-to-permanent         Create permanent from runtime configuration

## 端口控制
    firewall-cmd --list-all
    firewall-cmd --list-ports
    firewall-cmd --add-port=22/tcp --permanent
    firewall-cmd --remove-port=9022/tcp --permanent

## 端口转发
    firewall-cmd --add-masquerade --permanent       Enable IPv4 masquerade for a zone [P] [Z] [T]
    firewall-cmd --remove-masquerade --permanent    Disable IPv4 masquerade for a zone [P] [Z]
    firewall-cmd --query-masquerade                 Return whether IPv4 masquerading has been enabled for a zone [P] [Z]

    firewall-cmd --add-forward-port=port=53306:proto=tcp:toaddr=172.16.100.61:toport=3306 --permanent
    firewall-cmd --remove-forward-port=port=53306:proto=tcp --permanent
    firewall-cmd --query-forward-port=port=53306:proto=tcp


# 其他

## 常用软件
yum install wget
yum install net-tools
yum install mdadm

## 清理老版本
rpm -q kernel
rpm -e kernel-**************