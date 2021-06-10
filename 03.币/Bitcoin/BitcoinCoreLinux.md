## 安装
sudo tar -xzvf bitcoin-*.*.*-x86_64-linux-gnu.tar.gz -C /usr/local

## 创建配置文件
mkdir ~/.bitcoin
touch ~/.bitcoin/bitcoin.conf
chmod 600 ~/.bitcoin/bitcoin.conf

## 启动
cd /usr/local/bitcoin-*.*.*/bin
./bitcoind -daemon

./bitcoin-cli stop



