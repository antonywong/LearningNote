sudo docker pull mcr.microsoft.com/mssql/server:2022-latest

sudo mkdir /mnt/md0/SQLServer2022
sudo mkdir /mnt/md0/SQLServer2022/Data
sudo mkdir /mnt/md0/SQLServer2022/Backup
sudo mkdir /mnt/md0/SQLServer2022/log
sudo chmod 777 /mnt/md0/SQLServer2022/Data
sudo chmod 777 /mnt/md0/SQLServer2022/Backup
sudo chmod 777 /mnt/md0/SQLServer2022/log
sudo docker run -d --name SQLServer2022 -p 1433:1433 \
    -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=sql@0512" \
    -v /mnt/md0/SQLServer2022/Data:/var/opt/mssql/data \
    -v /mnt/md0/SQLServer2022/Backup:/var/opt/mssql/backup \
    -v /mnt/md0/SQLServer2022/log:/var/opt/mssql/log/ \
    -h SQLServer2022 --restart=always mcr.microsoft.com/mssql/server:2022-latest

> -h 用于显式设置容器主机名，如果不指定它，则默认为容器 ID，该 ID 是随机生成的系统 GUID。


sudo docker exec -u root -it SQLServer2022 bash


sudo docker rm SQLServer2022 -f
sudo rm -rf /mnt/md0/SQLServer2022/log

## Configure SQL Server on Linux with the mssql-conf tool
https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-configure-mssql-conf?view=sql-server-ver15

```
sudo docker exec -it SQLServer2022 bash
```
```
apt-get update
apt-get install sudo
apt-get install systemctl

/opt/mssql/bin/mssql-conf set sqlagent.enabled true 
systemctl restart mssql-server
```
