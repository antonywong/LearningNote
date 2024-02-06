# 命令

## 修改pacman源
sudo nano /etc/pacman.d/mirrorlist
### 中科大源
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
### manjaro自动更换
sudo pacman-mirrors -c China

## 常用命令
### 同步源
pacman -Sy
### 安装软件包
pacman -S package
### 搜索软件
pacman -Ss package
### 升级系统中的所有包
pacman -Syu
### 彻底卸载软件以及相关依赖
pacman -Rns 软件名称
### 查询已安装的包
pacman -Qs package
### 显示查找的包的信息
pacman -Qi package
### 显示你要找的包的文件都安装的位置
pacman -Ql package
### 下载但不安装包
pacman -Sw package
### 安装本地包
pacman -U /path/package.pkg.tar.gz
### 清理包缓存，下载的包会在/var/cache 这个目录
pacman -Scc
### 重新安装包
pacman -Sf pacman



# 配置
sudo nano /etc/pacman.conf

## Misc options
```
#UseSyslog
Color               #彩色输出
#NoProgressBar
CheckSpace
#VerbosePkgLists
ParallelDownloads = 5
```

## community源
```
[community]
Include = /etc/pacman.d/mirrorlist
```

## multilib源
```
[multilib]
Include = /etc/pacman.d/mirrorlist
```

## ArchLinuxCN源
```
[archlinuxcn]
SigLevel = Optional TrustAll
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
```
### 安装 archlinuxcn-keyring 包导入 GPG key。
sudo pacman -S archlinuxcn-keyring

## ArchLinuxFR源
```
[archlinuxfr]
Server = http://repo.archlinux.fr/$arch
```



# AUR

## AUR助手 yaourt
### 基础软件
sudo pacman -S base-devel fakeroot wget
### 安装 package-queryAUR
wget https://aur.archlinux.org/packages/pa/package-query/package-query.tar.gz
tar zxvf package-query.tar.gz
cd package-query
makepkg -si
cd ..
### 安装 yaourtAUR：
wget https://aur.archlinux.org/packages/ya/yaourt/yaourt.tar.gz
tar zxvf yaourt.tar.gz
cd yaourt
makepkg -si
cd ..

