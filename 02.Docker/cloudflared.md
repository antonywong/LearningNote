docker pull cloudflare/cloudflared

sudo mkdir /mnt/md0/cloudflare
sudo mkdir /mnt/md0/cloudflare/config
sudo chmod 777 /mnt/md0/cloudflare
sudo chmod 777 /mnt/md0/cloudflare/config
docker run -d --name cloudflared \
    -v /mnt/md0/cloudflare/config:/home/nonroot/.cloudflared \
    --restart=always cloudflare/cloudflared tunnel --no-autoupdate run

docker rm cloudflared -f


