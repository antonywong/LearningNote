sudo docker pull dorowu/ubuntu-desktop-lxde-vnc:focal

sudo docker run -d --name UbuntuDesktop -p 6080:80 -p 5900:5900 \
    -e VNC_PASSWORD=7 \
    -e RESOLUTION=1366x768 \
    -v /dev/shm:/dev/shm \
    --restart=always dorowu/ubuntu-desktop-lxde-vnc:focal


sudo docker rm UbuntuDesktop -f


