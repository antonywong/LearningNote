sudo docker pull v2ray/official

sudo mkdir /mnt/md0/v2ray
sudo mkdir /mnt/md0/v2ray/config
sudo mkdir /mnt/md0/v2ray/log
sudo chmod 777 /mnt/md0/v2ray/config
sudo chmod 777 /mnt/md0/v2ray/log
sudo docker run -d --name docker_v2ray -p 3128:3128 -p 3129:3129 \
    -v /mnt/md0/v2ray/config:/etc/v2ray \
    -v /mnt/md0/v2ray/log:/var/log/v2ray \
    --restart=always v2ray/official

sudo docker exec -it docker_v2ray /bin/bash

sudo docker cp docker_v2ray:/etc/v2ray/config.json .

sudo docker rm docker_v2ray -f