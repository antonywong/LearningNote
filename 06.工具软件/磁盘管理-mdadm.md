## 建立raid
sudo mdadm --create /dev/md0 --level=0 --raid-devices=3 /dev/sd{a,b}1 /dev/sdc4

## 设置开机挂载
sudo blkid /dev/md0
查看UUID
sudo nano /etc/fstab
UUID=72f38664-b5bb-4119-b667-8373fbe1826f /mnt/md0                ext4    defaults        0 0
修改配置

## 删除RAID
sudo cat /proc/mdstat
查看状态
sudo yum install psmisc
sudo fuser -vm /dev/md0
查看是否有用户正在使用该设备
sudo umount /dev/md0
sudo mdadm -S /dev/md0
停止md0的运行
sudo mdadm --zero-superblock /dev/sda1
清除组件设备sda1中超级块的信息



sudo mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/sd{a,b}1
sudo mkfs.ext4 -F /dev/md0
sudo rm -rf /mnt/md0
sudo mkdir /mnt/md0
sudo mount /dev/md0 /mnt/md0
sudo chmod 777 /mnt/md0
sudo blkid /dev/md0
sudo nano /etc/fstab
UUID=a2402955-7be5-4b72-bfdb-622acb63d053 /mnt/md0                ext4    defaults        0 0

sudo umount /dev/md0
sudo mdadm -S /dev/md0
sudo mdadm --zero-superblock /dev/sda4
sudo mdadm --zero-superblock /dev/sdb1
sudo mdadm --zero-superblock /dev/sdc1
sudo mdadm --zero-superblock /dev/sdd1

