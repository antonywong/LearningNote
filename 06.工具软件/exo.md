# 分布式AI运行工具

## 代理
export http_proxy="http://10.10.10.18:10809"
export https_proxy="http://10.10.10.18:10809"
export ALL_PROXY="http://10.10.10.18:10809"
export no_proxy="localhost,127.0.0.1,192.0.0.0/8,172.0.0.0/8,10.0.0.0/8"
export http_proxy=""
export https_proxy=""
export ALL_PROXY=""

## 系统工具
sudo pacman -S pyenv gcc make git
pyenv install 3.12.0

## 配置pip（可选）
nano .bashrc
```
export PATH=$PATH:/home/wangyj/.pyenv/versions/3.12.0/bin
```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install --upgrade pip

## 下载源代码
git clone git@github.com:exo-explore/exo.git

## 创建虚拟环境
python -m venv .exovenv
source .exovenv/bin/activate
deactivate
rm -rf .exovenv

## 安装依赖
cd exo
pip install -e .
### 安装
source install.sh
### 可能需要补充安装工具
sudo pacman -S mesa-utils clang
pip install llvmlite

## 运行
export HF_ENDPOINT=https://hf-mirror.com exo
cd ~
source .exovenv/bin/activate
cd exo
exo

## NFS网络磁盘（可选）
sudo pacman -S nfs-utils
sudo mount 10.10.10.120:/home/wangyj/.cache/exo/downloads /home/wangyj/.cache/exo/downloads
sudo nano /etc/fstab
```
# /home/wangyj/.cache/exo/downloads
10.10.10.120:/home/wangyj/.cache/exo/downloads /home/wangyj/.cache/exo/downloads nfs defaults 0 0
```
sudo mount -a

