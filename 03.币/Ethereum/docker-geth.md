# geth
sudo docker pull ethereum/client-go:stable

sudo mkdir /mnt/md0/geth
sudo mkdir /mnt/md0/geth/data
sudo chmod 777 /mnt/md0/geth
sudo chmod 777 /mnt/md0/geth/data
sudo docker run -d --name geth -p 8545:8545 -p 8546:8546 -p 30303:30303 \
    -v /mnt/md0/geth/data:/root/.ethereum/ \
    --restart=always ethereum/client-go:stable \
        --http --http.api personal,eth,net,web3 \
        --ws --ws.api personal,eth,net,web3 --ws.origins https://remix.ethereum.org


sudo docker exec -it geth /bin/sh
sudo docker exec -it geth geth --help
sudo docker exec -it geth geth attach /root/.ethereum/geth.ipc
sudo docker exec -it geth geth attach /root/.ethereum/geth.ipc --exec "net.peerCount"

sudo docker exec -it geth geth account --help
sudo docker exec -it geth geth account import /root/.ethereum/keyfile/metamask

sudo docker exec -it geth geth attach /root/.ethereum/geth.ipc --exec "eth.accounts"


sudo docker rm geth -f






nohup geth --rpc --rpcapi web3,eth,net,db,personal --rpcaddr 0.0.0.0 --rpcport 8545 


