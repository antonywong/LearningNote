# WSL

## 安装
https://learn.microsoft.com/zh-cn/windows/wsl/install-manual

## 管理
wsl --update
wsl --status
wsl --shutdown

## 位置迁移
wsl --export deepin D:\WSL\deepin_20250205_exo.tar
wsl --unregister deepin
wsl --import deepin D:\WSL\deepin D:\WSL\deepin_20250205.tar --version 2
### 设置默认用户
wsl -d deepin -u wangyj
如不成功则修改配置文件
nano /etc/wsl.conf
添加
```
[user]
default = wangyj
```