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


# bee-dashboard
sudo docker build . -t bee-dashboard
sudo docker run --name BeeDashboard --rm -p 8080:8080 bee-dashboard

sudo docker exec -it BeeDashboard /bin/sh

# bee
sudo docker pull ethersphere/bee:latest

sudo mkdir /mnt/md0/swarm
sudo mkdir /mnt/md0/swarm/bee
sudo chmod 777 /mnt/md0/swarm/bee
sudo docker run -d --name bee -p 1635:1635 -p 1634:1634 -p 1633:1633\
    -v /mnt/md0/swarm/bee:/home/bee/.bee \
    --rm -it ethersphere/bee:latest \
    start \
        --welcome-message="鸡蛋鸡蛋大鸡蛋！！！" \
        --swap-endpoint http://10.10.10.18:8545/ \
        --debug-api-enable

sudo docker rm bee -f


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
        --welcome-message="鸡蛋鸡蛋大鸡蛋！！！" \
        --swap-endpoint http://10.10.10.18:8545/ \
        --debug-api-enable
        

        