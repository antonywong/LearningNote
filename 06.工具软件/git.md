# GIT

## 配置
git config -l

## 代理
### HTTP 代理
git config --global http.proxy http://127.0.0.1:8080
### HTTPS 代理
git config --global https.proxy https://127.0.0.1:8080
### 使用 SOCKS5 代理
git config --global http.proxy socks5://10.10.10.18:10808
git config --global https.proxy socks5://10.10.10.18:10808

## 证书
C:\Users\home\.ssh\

## 命令
### 推送到主分支
git push origin master