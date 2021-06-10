# Install Bee Clef
wget https://github.com/ethersphere/bee-clef/releases/download/v0.4.12/bee-clef_0.4.12_amd64.rpm
sudo rpm -i bee-clef_0.4.12_amd64.rpm

systemctl status bee-clef


# Install Bee
wget https://github.com/ethersphere/bee/releases/download/v0.6.1/bee_0.6.0_amd64.rpm
sudo rpm -i bee_0.6.0_amd64.rpm

# 重要配置项
full-node: true
## 远程的Ethereum Goerli testnet blockchain
swap-endpoint: wss://goerli.infura.io/ws/v3/460e30f8d43841aaa9fb0b1c6a646e26
## 远程的ENS
resolver-options: ["https://mainnet.infura.io/v3/460e30f8d43841aaa9fb0b1c6a646e26"]
## 读写数据库的速度限制
db-open-files-limit: 2000