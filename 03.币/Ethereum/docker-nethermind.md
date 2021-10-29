# nethermind
sudo docker pull nethermind/nethermind:latest

sudo mkdir /mnt/md0/xdai
sudo mkdir /mnt/md0/xdai/nethermind_db
sudo mkdir /mnt/md0/xdai/logs
sudo mkdir /mnt/md0/xdai/keystore
sudo chmod 777 /mnt/md0/xdai
sudo chmod 777 /mnt/md0/xdai/nethermind_db
sudo chmod 777 /mnt/md0/xdai/logs
sudo chmod 777 /mnt/md0/xdai/keystore

sudo docker run -d --name xdai -p 8545:8545 -p 30303:30303 \
    -v /mnt/md0/xdai/nethermind_db:/nethermind/nethermind_db/ \
    -v /mnt/md0/xdai/logs:/nethermind/logs/ \
    -v /mnt/md0/xdai/keystore:/nethermind/keystore/ \
    --restart=always nethermind/nethermind:latest \
        --datadir data --config xdai --JsonRpc.Enabled true --JsonRpc.Host 0.0.0.0


sudo docker exec -it xdai /bin/sh


sudo docker rm xdai -f




