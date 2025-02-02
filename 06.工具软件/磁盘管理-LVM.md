## 查看pv分区
sudo pvscan

## pv分区
sudo pvcreate /dev/sdb1
sudo pvremove /dev/sdb1

## 新建逻辑卷组
sudo vgcreate

## 将新分区添加到pv分区
sudo vgextend  VolumeGroupName  PhysicalDevicePath




