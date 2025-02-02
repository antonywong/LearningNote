sudo mkdir /mnt/md0/v2fly
sudo mkdir /mnt/md0/v2fly/share
sudo mkdir /mnt/md0/v2fly/config
sudo chmod 777 /mnt/md0/v2fly/share
sudo chmod 777 /mnt/md0/v2fly/config

docker pull v2fly/v2fly-core
docker rm v2fly -f
docker run -d --name v2fly -p 10808:10808 -p 10809:10809 \
    -v /mnt/md0/v2fly/share:/usr/local/share/v2ray \
    -v /mnt/md0/v2fly/config:/etc/v2ray \
    --restart=always v2fly/v2fly-core run -c /etc/v2ray/config.json

docker exec -it v2fly /bin/sh