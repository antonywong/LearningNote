## 更换源
cd /etc/yum.repos.d/
sudo mkdir backup/
sudo cp fedora.repo backup/
sudo cp fedora-modular.repo backup/
sudo cp fedora-updates.repo backup/
sudo cp fedora-updates-modular.repo backup/

sudo sed -e 's|^metalink=|#metalink=|g' \
         -e 's|^#baseurl=http://download.example/pub/fedora/linux|baseurl=https://mirrors.tuna.tsinghua.edu.cn/fedora|g' \
         /etc/yum.repos.d/fedora.repo \
         /etc/yum.repos.d/fedora-modular.repo \
         /etc/yum.repos.d/fedora-updates.repo \
         /etc/yum.repos.d/fedora-updates-modular.repo

sudo dnf makecache

## 命令
### 查看 DNF 包管理器版本
dnf --version
### 查看系统中可用的 DNF 软件库
dnf repolist
### 查看系统中可用和不可用的所有的 DNF 软件库
dnf repolist all
### 列出所有 RPM 包
dnf list
### 列出所有安装了的 RPM 包
dnf list installed
### 列出所有可供安装的 RPM 包
dnf list available
### 搜索软件库中的 RPM 包
dnf search nano
### 查找某一文件的提供者
dnf provides /bin/bash
### 查看软件包详情
dnf info nano
### 安装软件包
dnf install nano
### 升级软件包
dnf update systemd
### 检查系统软件包的更新
dnf check-update
### 更新本地缓存
dnf makecache
### 升级所有系统软件包
dnf update 或 dnf upgrade
### 删除软件包
dnf remove nano 或 dnf erase nano
### 删除无用孤立的软件包
dnf autoremove
### 删除缓存的无用软件包
dnf clean all
### 获取有关某条命令的使用帮助
dnf help clean
### 查看所有的 DNF 命令及其用途
dnf help
### 查看 DNF 命令的执行历史
dnf history
### 查看所有的软件包组
dnf grouplist
### 安装一个软件包组
dnf groupinstall 'Educational Software'
### 升级一个软件包组中的软件包
dnf groupupdate 'Educational Software'
### 删除一个软件包组
dnf groupremove 'Educational Software'
### 从特定的软件包库安装特定的软件
dnf --enablerepo=epel install phpmyadmin
### 更新软件包到最新的稳定发行版
dnf distro-sync
### 重新安装特定软件包
dnf reinstall nano
### 回滚某个特定软件的版本
dnf downgrade acpid