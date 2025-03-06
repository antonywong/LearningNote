# system
## 设置网络
ip link
sudo nano /etc/systemd/network/20-wired.network
```
[Match]
Name=enp1s0

[Network]
Address=192.168.2.105/24
Gateway=192.168.2.2
DNS=61.177.7.1
```
sudo systemctl enable --now systemd-networkd
sudo systemctl restart systemd-networkd

sudo nano /etc/resolv.conf
```
nameserver 221.228.255.1
nameserver 61.177.7.1
```
sudo systemctl enable --now systemd-resolved
sudo systemctl restart systemd-resolved
sudo resolvectl status


## 新建用户/密码
useradd -m -s /bin/bash wangyj
passwd wangyj

## 用户组
### 查看所有用户
cat /etc/passwd
### 查看所有组
cat /etc/group
### 查看账号所在组
groups
### 删除用户组
sudo groupdel wangyj

## sudoer
sudo pacman -S sudo
sudo nano /etc/sudoers
```
wangyj ALL=(ALL) ALL
```

## SSH
sudo pacman -S openssh
sudo systemctl enable --now sshd

## 笔记本不进入休眠
sudo nano /etc/systemd/logind.conf
```
HandleLidSwitch=ignore
```



# docker
## 安装
sudo pacman -S docker

## 将本地用户加入 docker 组
sudo usermod -aG docker $USER
newgrp docker

## 启动服务
sudo systemctl enable docker
sudo systemctl start docker
systemctl status docker

## 更换目录位置
sudo systemctl stop docker
sudo cp -r /var/lib/docker /home/docker
sudo rm -rf /var/lib/docker
sudo ln -s /home/docker /var/lib/docker
sudo systemctl start docker



# GNOME

## 显卡驱动
```
extra/xf86-video-amdgpu 23.0.0-1 (xorg-drivers)
extra/xf86-video-ati 1:22.0.0-1 (xorg-drivers)
extra/xf86-video-dummy 0.4.1-1 (xorg-drivers)
extra/xf86-video-fbdev 0.5.0-3 (xorg-drivers)
extra/xf86-video-intel 1:2.99.917+923+gb74b67f0-1 (xorg-drivers)
extra/xf86-video-nouveau 1.0.17-2 (xorg-drivers)
extra/xf86-video-openchrome 0.6.0.r798.g0c75274-2 (xorg-drivers)
extra/xf86-video-qxl 0.1.6-1 (xorg-drivers)
extra/xf86-video-sisusb 0.9.7-4
extra/xf86-video-vesa 2.6.0-1 (xorg-drivers xorg)
extra/xf86-video-vmware 13.4.0-1 (xorg-drivers)
extra/xf86-video-voodoo 1.2.6-1 (xorg-drivers)
```
sudo pacman -S xf86-video-vmware

## Xorg
sudo pacman -S xorg

## GNOME
sudo pacman -S gnome

# gdm开机启动
sudo systemctl enable gdm



# VMware-Tools
sudo pacman -S open-vm-tools
sudo systemctl enable vmtoolsd


# VNC

## 安装
sudo pacman -S tigervnc

## 启动 VNC Server
### 设置密码
vncpasswd
### 启动
vncserver :0



# kvm

## 前期准备
### 检查虚拟化
egrep -o 'vmx|svm' /proc/cpuinfo
### 检查KVM
zgrep KVM /proc/config.gz
### 检查VIRTIO
zgrep VIRTIO /proc/config.gz
### 当前用户加入kvm组
sudo usermod -aG kvm $USER

## 安装
sudo pacman -S qemu libvirt dnsmasq virt-manager bridge-utils flex bison iptables-nft edk2-ovmf
### 查看模块是否运行
lsmod | grep kvm
### 开启kvm服务
sudo systemctl enable --now libvirtd
sudo systemctl status libvirtd
