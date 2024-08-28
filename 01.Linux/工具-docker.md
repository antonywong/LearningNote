## 将本地用户加入 docker 组
sudo usermod -aG docker $USER
newgrp docker

## 国内源
### 修改配置
sudo mkdir /etc/docker
sudo nano /etc/docker/daemon.json
```
{
    "registry-mirrors": [
            "https://docker.m.daocloud.io",
            "https://docker.nju.edu.cn",
            "https://dockerproxy.com"
    ]
}
```

## 更换目录位置
sudo systemctl stop docker
sudo cp -rp /var/lib/docker /mnt/md0/DOCKER_HOME
sudo rm -rf /var/lib/docker
sudo ln -s /mnt/md0/DOCKER_HOME /var/lib/docker
sudo systemctl start docker

## 加载重启docker
sudo systemctl restart docker
sudo systemctl stop docker
sudo systemctl disable docker

## 查看是否成功
sudo docker info
