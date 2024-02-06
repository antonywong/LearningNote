# 准备

## 查看是否支持虚拟化
cat /proc/cpuinfo
### for Intel CPU
cat /proc/cpuinfo | grep vmx
### for AMD CPU
cat /proc/cpuinfo | grep svm

## 安装KVM
### ARCH
sudo pacman -S qemu libvirt dnsmasq virt-manager bridge-utils flex bison iptables-nft edk2-ovmf
### UBUNTU DEBIAN
sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager libguestfs-tools
### CENTOS RHEL FEDORA
sudo yum install libvirt qemu-kvm

## 启动KVM
sudo systemctl enable --now libvirtd
sudo systemctl enable --now virtlogd
echo 1 | sudo tee /sys/module/kvm/parameters/ignore_msrs
sudo modprobe kvm

# 安装

## pull，latest对应的是Catalina
sudo docker pull sickcodes/docker-osx:latest
sudo docker pull sickcodes/docker-osx:big-sur

## run
sudo docker run -it \
    --device /dev/kvm \
    -p 50922:10022 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e "DISPLAY=${DISPLAY:-:0.0}" \
    sickcodes/docker-osx:latest

