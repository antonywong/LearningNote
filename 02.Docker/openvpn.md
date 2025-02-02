sudo mkdir /mnt/md0/openvpn
sudo chmod 777 /mnt/md0/openvpn

docker pull openvpn/openvpn-as
docker rm openvpn-as -f
docker run -d --name openvpn-as --device /dev/net/tun --cap-add=MKNOD --cap-add=NET_ADMIN \
    -p 943:943 -p 9001:443 -p 1194:1194/udp -v /mnt/md0/openvpn:/openvpn \
    --env HTTP_PROXY="http://172.18.0.2:10809" --env HTTPS_PROXY="http://172.18.0.2:10809" --env ALL_PROXY="http://172.18.0.2:10809" \
    --restart=always --network toshiba --network-alias openvpn openvpn/openvpn-as

docker exec -it openvpn-as /bin/bash
sacli --user "openvpn" --new_pass "p10" SetLocalPassword