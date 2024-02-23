# 安装

## 镜像
sudo docker pull dreamacro/clash

sudo mkdir /mnt/md0/clash
sudo mkdir /mnt/md0/clash/ui
sudo mkdir /mnt/md0/clash/data
sudo touch /mnt/md0/clash/data/config.yaml
sudo chmod 777 /mnt/md0/clash/ui
sudo chmod 777 /mnt/md0/clash/data
sudo docker run -d --name clash -p 7890:7890 -p 7891:7891 -p 9090:9090 \
    -v /mnt/md0/clash/data:/root/.config/clash
    -v /mnt/md0/clash/ui:/ui \
    --restart=always dreamacro/clash

## 配置
docker exec -it clash sh

## 删除
docker rm clash -f



# 配置
## UI
1.yacd
2.clash-dashboard-gh-pages

## config.yaml
```
mixed-port: 7890
allow-lan: true
mode: Rule
log-level: info
external-controller: '0.0.0.0:9090'
external-ui: /ui
Proxy:
Proxy Group:
Rule:
secret:
proxies:
  - name: "vmess"
    type: vmess
    server: server
    port: 443
    uuid: uuid
    alterId: 0
    cipher: auto
    network: ws
    tls: true
    # udp: false
    skip-cert-verify: false
    servername: servername
    ws-opts:
      path: /vm
      headers:
        Host: Host
    # max-early-data: 2048
    # early-data-header-name: Sec-WebSocket-Protocol

  - name: "socks"
    type: socks5
    # interface-name: eth0
    # routing-mark: 1234
    server: 127.0.0.1
    port: 10808
    # username: username
    # password: password
    # tls: true
    # skip-cert-verify: true
    # udp: true
```

