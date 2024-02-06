# 防火墙

## 服务
systemctl start firewalld
systemctl stop firewalld
systemctl enable firewalld
systemctl disable firewalld
systemctl status firewalld

## 重新加载
firewall-cmd --state                        Return and print firewalld state
firewall-cmd --reload                       Reload firewall and keep state information
firewall-cmd --complete-reload              Reload firewall and lose state information
firewall-cmd --runtime-to-permanent         Create permanent from runtime configuration

## 端口控制
firewall-cmd --list-all
firewall-cmd --list-ports
firewall-cmd --add-port=53391/tcp --permanent
firewall-cmd --remove-port=53389/tcp --permanent

## 端口转发
firewall-cmd --add-masquerade --permanent       Enable IPv4 masquerade for a zone [P] [Z] [T]
firewall-cmd --remove-masquerade --permanent    Disable IPv4 masquerade for a zone [P] [Z]
firewall-cmd --query-masquerade                 Return whether IPv4 masquerading has been enabled for a zone [P] [Z]

firewall-cmd --add-port=4520-4529/tcp --permanent
firewall-cmd --add-forward-port=port=53389:proto=tcp:toaddr=172.16.100.6:toport=3389 --permanent
firewall-cmd --remove-forward-port=port=50022:proto=tcp:toaddr=127.0.0.1:toport=22 --permanent
firewall-cmd --query-forward-port=port=53306:proto=tcp

firewall-cmd --remove-forward-port=port=51433:proto=tcp:toport=1433:toaddr=172.16.100.7 --permanent
firewall-cmd --add-forward-port=port=51433:proto=tcp:toport=3306:toaddr=172.16.100.62 --permanent
