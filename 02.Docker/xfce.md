sudo docker pull ubuntu:22.04


sudo docker rm docker_ubuntu2204 -f


sudo docker run -itd --name docker_ubuntu2204 -p 15901:5901 \
    --restart=always ubuntu:22.04

sudo docker exec -it docker_ubuntu2204 /bin/bash





cp /etc/apt/sources.list /etc/apt/sources.list.bak

echo "
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
" > /etc/apt/sources.list



unminimize



apt install language-pack-zh-hans -y

echo 'LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh:en_US:en"' >> /etc/environment

echo 'LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh:en_US:en"' >> /etc/profile

echo 'LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh:en_US:en"' >> ~/.bashrc

locale-gen

source ~/.bashrc



apt install -y tigervnc-standalone-server xubuntu-desktop \
    dbus-x11 \
    fonts-wqy-microhei \
    gnome-user-docs-zh-hans \
    language-pack-gnome-zh-hans \
    fcitx \
    fcitx-pinyin \
    fcitx-table-wubi



adduser wangyj

su wangyj

vncpasswd

echo '#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export LANG=zh_CN.UTF-8
fcitx -r
startxfce4' > ~/.vnc/xstartup

chmod u+x ~/.vnc/xstartup



vncserver :1 -localhost no -geometry=1920x1080


