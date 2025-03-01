## 备份源
sudo cp /etc/apt/sources.list.d/antix.list /etc/apt/sources.list.d/antix.list.bak
sudo cp /etc/apt/sources.list.d/bullseye-backports.list /etc/apt/sources.list.d/bullseye-backports.list.bak
sudo cp /etc/apt/sources.list.d/debian.list /etc/apt/sources.list.d/debian.list.bak
sudo cp /etc/apt/sources.list.d/debian-stable-updates.list /etc/apt/sources.list.d/debian-stable-updates.list.bak

### 新建源
sudo echo "
deb https://mirrors.tuna.tsinghua.edu.cn/mxlinux/antix/bullseye bullseye main nosystemd nonfree
" > /etc/apt/sources.list.d/antix.list

sudo echo "
deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye-backports main contrib non-free
" > /etc/apt/sources.list.d/bullseye-backports.list

sudo echo "
deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
" > /etc/apt/sources.list.d/debian.list

sudo echo "
deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye-updates main contrib non-free
" > /etc/apt/sources.list.d/debian-stable-updates.list


## Docker
### 下载签名证书
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-archive-keyring.gpg

### 增加库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian/ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


## 安装
sudo apt-get install docker-ce docker-ce-cli containerd.io


## 请将本地用户加入 docker 组
sudo usermod -aG docker $USER
newgrp docker

