## docker
### 安装必要组件
sudo apt install ca-certificates curl gnupg lsb-release
### 下载签名证书
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-archive-keyring.gpg
### 增加库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
### 安装
sudo apt-get install docker-ce docker-ce-cli containerd.io

## SSH
安装  
apt-get install ssh
初始化密钥  
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

## ssh端口修改
sudo nano /etc/ssh/sshd_config
systemctl restart sshd.service

## 网络设置
修改/etc/network/interfaces，格式：  
auto eth0  
face eth0 inet static  
address 192.168.222.111  
gateway 192.168.222.1  
netmask 255.255.255.0  
dns-nameservers 221.228.255.1 61.177.7.1  

重启网络服务
sudo /etc/init.d/networking restart