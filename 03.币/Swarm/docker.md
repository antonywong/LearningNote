# bee-clef
sudo docker pull ethersphere/clef:latest

sudo mkdir /mnt/md0/swarm
sudo mkdir /mnt/md0/swarm/bee-clef
sudo mkdir /mnt/md0/swarm/bee-clef/data
sudo chmod 777 /mnt/md0/swarm/bee-clef
sudo chmod 777 /mnt/md0/swarm/bee-clef/data
sudo docker run -d --name bee-clef -p 8550:8550 \
    -v /mnt/md0/swarm/bee-clef/data:/app/data \
    --restart=always ethersphere/clef:latest

sudo docker exec -it bee-clef /bin/bash
clef init --configdir "/app/data"

sudo docker rm bee-clef -f


# bee
sudo docker pull ethersphere/bee:latest

sudo mkdir /mnt/md0/swarm
sudo mkdir /mnt/md0/swarm/bee
sudo chmod 777 /mnt/md0/swarm/bee
sudo docker run -d --name bee -p 1635:1635 -p 1634:1634 -p 1633:1633\
    -v /mnt/md0/swarm/bee:/home/bee/.bee \
    --rm -it ethersphere/bee:latest \
    start \
        --welcome-message="Bzzzz bzzz bzz bzz. 🐝" \
        --swap-endpoint wss://goerli.infura.io/ws/v3/460e30f8d43841aaa9fb0b1c6a646e26 \
        --debug-api-enable

curl localhost:1633
curl -s localhost:1635/peers | jq ".peers | length"
curl -X GET http://localhost:1635/topology | jq

curl localhost:1635/chequebook/balance | jq
curl localhost:1635/chequebook/cheque | jq

curl localhost:1635/balances | jq

/faucet sprinkle 5f51389ee5ce69e1558eef89ad84490e28374c92

sudo docker exec -it bee bee --help




sudo docker run --name bee -p 1635:1635 -p 1634:1634 -p 1633:1633\
    -v /mnt/md0/swarm/bee:/home/bee/.bee \
    --rm -it ethersphere/bee:latest \
    start \
        --welcome-message="Bzzzz bzzz bzz bzz. 🐝" \
        --swap-endpoint wss://goerli.infura.io/ws/v3/460e30f8d43841aaa9fb0b1c6a646e26 \
        --debug-api-enable