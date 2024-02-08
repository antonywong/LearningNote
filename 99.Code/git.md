# 配置

## 配置列表
git config --list --show-origin
git config --list --local
git config --list --global
git config --list --system

## 加基础配置
git config --system user.name 'antony_wong'
git config --system user.email 'antony_wong@msn.com'

## 加代理
git config --system https.proxy 'socks5://10.10.10.18:7890'



# SSH

## ssh
ssh-keygen -t ed25519 -C "antony_wong@msn.com"

~/.ssh/wangyj-pc

## config
~/.ssh/config
```
Host github.com
IdentityFile ~/.ssh/wangyj-pc
```

## 测试github
ssh -T git@github.com
ssh -Tv git@github.com


