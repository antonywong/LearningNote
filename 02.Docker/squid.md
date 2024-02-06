sudo docker search ubuntu/squid

sudo docker pull ubuntu/squid

sudo mkdir /mnt/md0/squid
sudo touch /mnt/md0/squid/squid.conf
sudo chmod 777 /mnt/md0/squid/squid.conf
sudo docker run -d --name docker_squid -e TZ=UTC -p 33128:3128 \
    -v /mnt/md0/squid/squid.conf:/etc/squid/squid.conf \
    --restart=always ubuntu/squid

sudo docker exec -it docker_squid /bin/bash

sudo docker cp docker_squid:/etc/squid/squid.conf .

sudo docker rm docker_squid -f