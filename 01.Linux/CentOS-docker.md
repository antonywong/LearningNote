sudo yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine

sudo yum install -y yum-utils \
    device-mapper-persistent-data \
    lvm2

sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io

sudo systemctl start docker

sudo systemctl enable docker