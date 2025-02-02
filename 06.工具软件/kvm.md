# manjaro

## 前期准备
### 检查虚拟化
LC_ALL=C lscpu | grep Virtualization
### 检查KVM
zgrep CONFIG_KVM /proc/config.gz
lsmod | grep kvm

## 安装
sudo pacman -S qemu libvirt virt-manager edk2-ovmf qemu-arch-extra
### 开启kvm服务
sudo systemctl enable --now libvirtd
sudo systemctl status libvirtd

