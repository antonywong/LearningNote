sudo docker search nginx

sudo docker pull nginx

sudo mkdir /mnt/md0/nginx
sudo mkdir /mnt/md0/nginx/html
sudo mkdir /mnt/md0/nginx/logs
sudo touch /mnt/md0/nginx/nginx.conf
sudo chmod 777 /mnt/md0/nginx
sudo chmod 777 /mnt/md0/nginx/html
sudo chmod 777 /mnt/md0/nginx/logs
sudo chmod 777 /mnt/md0/nginx/nginx.conf
sudo docker run -d --name docker_nginx -p 30080:80 \
    -v /mnt/md0/nginx/html:/usr/share/nginx/html \
    -v /mnt/md0/nginx/nginx.conf:/etc/nginx/nginx.conf \
    -v /mnt/md0/nginx/logs:/var/log/nginx \
    --restart=always nginx

sudo docker exec -it docker_nginx /bin/bash

sudo docker cp docker_nginx:/etc/nginx/nginx.conf /mnt/md0/nginx

sudo docker rm docker_nginx -f


