sudo docker pull mcr.microsoft.com/mssql/server:2019-latest

sudo mkdir /mnt/md0/SQLServer2019
sudo mkdir /mnt/md0/SQLServer2019/Data
sudo mkdir /mnt/md0/SQLServer2019/Backup
sudo chmod 777 /mnt/md0/SQLServer2019/Data
sudo chmod 777 /mnt/md0/SQLServer2019/Backup
sudo docker run -d --name sqlserver2019 -p 1433:1433 \
    -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=sql@0512" \
    -v /mnt/md0/SQLServer2019/Data:/var/opt/mssql/data \
    -v /mnt/md0/SQLServer2019/Backup:/var/opt/mssql/backup \
    -h sqlserver2019 --restart=always mcr.microsoft.com/mssql/server:2019-latest

> -h 用于显式设置容器主机名，如果不指定它，则默认为容器 ID，该 ID 是随机生成的系统 GUID。

sudo docker rm sqlserver2019 -f