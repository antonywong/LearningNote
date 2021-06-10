sudo docker pull portainer/portainer-ce

sudo docker run -d --name portainerUI -p 9000:9000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --restart=always portainer/portainer-ce

sudo docker rm portainerUI -f