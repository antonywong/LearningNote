sudo yum install cifs-utils

sudo mkdir /mnt/download
sudo chmod 777 /mnt/download

sudo vi /etc/fstab
//10.10.10.17/Download   /mnt/download cifs auto, username=wangyj,password=Ch@202105 0 0
sudo mount -a


sudo mount.cifs //192.168.2.7/a/ /mnt/md0/jellyfin/media/ -o user=home,pass=1


