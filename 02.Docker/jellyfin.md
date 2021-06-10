sudo docker search jellyfin
sudo docker pull jellyfin/jellyfin

sudo mkdir /mnt/md0/jellyfin
sudo mkdir /mnt/md0/jellyfin/media
sudo chmod 777 /mnt/md0/jellyfin/media

sudo docker run -d --name jellyfin -p 8096:8096 \
    -v /mnt/md0/jellyfin/config:/config \
    -v /mnt/md0/jellyfin/media:/media \
    --restart=always jellyfin/jellyfin

sudo docker rm jellyfin -f





sudo mkdir /mnt/md0/jellyfin
sudo mkdir /mnt/md0/jellyfin/media
sudo chmod 777 /mnt/md0/jellyfin/media
sudo docker run -d --name jellyfin -p 8096:8096 \
    -v /mnt/md0/jellyfin/config:/config \
    -v /mnt/md0/collection:/media \
    --restart=always jellyfin/jellyfin