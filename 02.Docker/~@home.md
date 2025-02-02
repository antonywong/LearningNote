docker network create toshiba

# samba
sudo mkdir /mnt/md0/samba
sudo chmod 777 /mnt/md0/samba

docker pull dperson/samba
docker rm samba -f
docker run -d --name samba -p 139:139 -p 445:445 \
    -v /mnt/md0:/mount \
    --restart=always dperson/samba \
    -u "home;7" \
    -s "docker;/mount/;yes;no;no;all;none;home"

# portainer
sudo mkdir /mnt/md0/portainer
sudo mkdir /mnt/md0/portainer/data
sudo chmod 777 /mnt/md0/portainer/data

docker pull portainer/portainer-ce
docker rm portainer -f
docker run -d --name portainer -p 9000:9000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /mnt/md0/portainer/data:/data \
    --restart=always portainer/portainer-ce

# nginx
sudo mkdir /mnt/md0/nginx
sudo chmod 777 /mnt/md0/nginx

docker pull nginx
docker rm docker_nginx -f
docker run -d --name docker_nginx -p 80:80 -p 443:443 \
    -v /mnt/md0/nginx/conf:/etc/nginx \
    -v /mnt/md0/nginx/html:/usr/share/nginx/html \
    -v /mnt/md0/nginx/logs:/var/log/nginx \
    --restart=always nginx

# cloudflared-client-vmess-60023
docker pull cloudflare/cloudflared
docker rm cloudflared-client-vmess-60023 -f
docker run -d --name cloudflared-client-vmess-60023 -p 60023:60023 \
    --restart=always --network toshiba --network-alias cloudflared-client-vmess-60023 \
    cloudflare/cloudflared access tcp --hostname ser00vmess.hemuduegg.eu.org --url 0.0.0.0:60023

# v2fly
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
    --restart=always --network toshiba --network-alias v2fly \
    v2fly/v2fly-core run -c /etc/v2ray/config.json
