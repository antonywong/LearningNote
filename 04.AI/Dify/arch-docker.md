# 安装docker
sudo pacman -Syu docker docker-compose


# 安装

## clone
git clone git@github.com:langgenius/dify.git
cd dify/docker/

## 复制环境配置文件
cp .env.example .env

## 启动 Docker 容器
docker compose up -d
docker compose ps

