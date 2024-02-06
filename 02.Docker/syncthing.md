sudo docker search linuxserver/syncthing

sudo docker pull linuxserver/syncthing

sudo mkdir /mnt/md0/syncthing
sudo mkdir /mnt/md0/syncthing/data1
sudo mkdir /mnt/md0/syncthing/data2
sudo mkdir /mnt/md0/syncthing/config
sudo docker run -d --name docker_syncthing --hostname docker_syncthing -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC \
    -p 8384:8384 -p 22000:22000/tcp -p 22000:22000/udp -p 21027:21027/udp \
    -v /mnt/md0/syncthing/config:/config \
    -v /mnt/md0/syncthing/data1:/data1 \
    -v /mnt/md0/syncthing/data2:/data2 \
    --restart=always linuxserver/syncthing


sudo docker exec -it docker_syncthing /bin/bash

sudo docker cp docker_syncthing:/etc/squid/squid.conf .

sudo docker rm docker_syncthing -f


