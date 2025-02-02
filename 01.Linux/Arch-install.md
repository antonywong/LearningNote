# 安装
## 查看IP地址
ip address

## 磁盘分区
fdisk /dev/sda
SWAP分区的partition type设为GUID 0657FD6D-A4AB-43C4-84E5-0933C84B4F4F(Linux swap)
### BIOS with GPT
创建1兆的分区(+1M with fdisk)，partition type设为GUID 21686148-6449-6E6F-744E-656564454649(BIOS boot).
```
sda1    1M    
sda2    4096M   [SWAP]
sda3    rest    /
```
### UEFI with GPT
创建启动分区(300M-1024M)，partition type设为GUID C12A7328-F81F-11D2-BA4B-00A0C93EC93B(EFI System).
```
sda1    500M    /boot
sda2    8192M   [SWAP]
sda3    rest    /
```
### 查看分区表
fdisk -l

## 格式化分区
mkfs.fat -F 32 /dev/sda1
mkswap /dev/sda2
mkfs.ext4 /dev/sda3

## 挂载目录
swapon /dev/sda2
mount /dev/sda3 /mnt

## 修改pacman源
vim /etc/pacman.d/mirrorlist
### 中科大源
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch

## 安装base package, Linux kernel and firmware for common hardware
pacstrap -K /mnt base linux linux-firmware

## UEFI启动，挂载启动分区
mount --mkdir /dev/sda1 /mnt/boot/efi

## 生成fstab文件
genfstab -U /mnt >> /mnt/etc/fstab
cat /mnt/etc/fstab

## 进入新系统
arch-chroot /mnt

## 设置时区
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
### 生成/etc/adjtime
hwclock --systohc

## 同步pacman
pacman -Sy
pacman -S nano sudo openssh

## 本地化，编辑/etc/locale.gen，去除具体地区（zh_CN.UTF-8 UTF-8）的注释
nano /etc/locale.gen
locale-gen
echo "LANG=zh_CN.UTF-8" >> /etc/locale.conf
echo "LANG=en_US.UTF-8" >> /etc/locale.conf

## 生成hostname文件:
echo "wangyj-arch" >> /etc/hostname

## 设置网络
ip link
nano /etc/systemd/network/20-wired.network
```
[Match]
Name=enp3s0

[Network]
Address=192.168.11.100/24
Gateway=192.168.11.1
DNS=192.168.0.1
```

nano /etc/resolv.conf
```
nameserver 192.168.0.1
nameserver 221.228.255.1
nameserver 61.177.7.1
```

## 新建用户/密码
useradd -m -s /bin/bash wangyj 
passwd wangyj

## sudoer
nano /etc/sudoers
```
wangyj ALL=(ALL) ALL
```

## 设置开机启动服务
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable sshd



# BIOS固件启动
pacman -S grub
grub-install --target=i386-pc /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg



# UEFI固件启动
pacman -S grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg


