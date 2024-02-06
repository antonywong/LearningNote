sudo docker pull mysql

sudo docker run -d --name mysql -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=sql@0512 \
    --restart=always mysql

sudo docker rm mysql -f