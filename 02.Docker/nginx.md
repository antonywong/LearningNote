docker pull nginx

sudo mkdir /mnt/md0/nginx
sudo chmod 777 /mnt/md0/nginx
docker run -d --name docker_nginx -p 80:80 -p 443:443 \
    -v /mnt/md0/nginx/conf:/etc/nginx \
    -v /mnt/md0/nginx/html:/usr/share/nginx/html \
    -v /mnt/md0/nginx/logs:/var/log/nginx \
    --restart=always nginx

docker exec -it docker_nginx /bin/bash

docker rm docker_nginx -f



docker run -d --name docker_nginx -p 80:80 --restart=always nginx
docker cp docker_nginx:/etc/nginx            /mnt/md0/nginx
mv /mnt/md0/nginx/nginx /mnt/md0/nginx/conf
docker cp docker_nginx:/usr/share/nginx/html /mnt/md0/nginx
docker cp docker_nginx:/var/log/nginx        /mnt/md0/nginx
mv /mnt/md0/nginx/nginx /mnt/md0/nginx/logs
docker rm docker_nginx -f

