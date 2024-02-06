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
systemctl restart sshd

## 检查sshd服务是否已经开启
ps -e | grep sshd



# docker

## 清理老版本
sudo yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine

## 安装必备组件
sudo yum install -y yum-utils \
    device-mapper-persistent-data \
    lvm2

## 配置国内下载源
sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

## 安装和启动
sudo yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker



# 其他

## 清理老版本
rpm -q kernel
rpm -e kernel-**************