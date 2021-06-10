sudo docker search nginx

sudo docker pull nginx

mkdir /mnt/md0/nginx
mkdir /mnt/md0/nginx/html
mkdir /mnt/md0/nginx/logs
touch /mnt/md0/nginx/nginx.conf
sudo docker run -d --name docker_nginx -p 30080:80 \
    -v /mnt/md0/nginx/html:/usr/share/nginx/html \
    -v /mnt/md0/nginx/nginx.conf:/etc/nginx/nginx.conf \
    -v /mnt/md0/nginx/logs:/var/log/nginx \
    --restart=always nginx

sudo docker rm docker_nginx -f