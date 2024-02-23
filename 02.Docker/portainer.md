docker pull portainer/portainer-ce

sudo mkdir /mnt/md0/portainer
sudo mkdir /mnt/md0/portainer/data
sudo chmod 777 /mnt/md0/portainer/data
docker run -d --name portainer -p 9000:9000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /mnt/md0/portainer/data:/data \
    --restart=always portainer/portainer-ce

docker rm portainer -f

docker start portainer
docker stop portainer