# 定时任务
sudo pacman -Sy cronie
sudo yum install cronie
sudo apt-get install cron

## 服务
sudo systemctl enable cronie
sudo systemctl start cronie
sudo systemctl stop cronie
sudo systemctl disable cronie

sudo systemctl enable crond
sudo systemctl start crond
sudo systemctl enable cron
sudo systemctl start cron

## 