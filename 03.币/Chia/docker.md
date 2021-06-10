docker pull ghcr.io/chia-network/chia:latest

# Official Chia Docker Container

## Basic Startup
docker run --name <container-name> -d ghcr.io/chia-network/chia:latest
(optional -v /path/to/plots:plots)

## Configuration

### You can modify the behavior of your Chia container by setting specific environment variables.
### To use your own keys pass as arguments on startup (post 1.0.2 pre 1.0.2 must manually pass as shown below)
-v /path/to/key/file:/path/in/container -e keys="/path/in/container"

### or pass keys into the running container
docker exec -it <container-name> venv/bin/chia keys add

### alternatively you can pass in your local keychain, if you have previously deployed chia with these keys on the host machine
-v ~/.local/share/python_keyring/:/root/.local/share/python_keyring/

### To start a farmer only node pass
-e farmer="true"

### To start a harvester only node pass
-e harvester="true" -e farmer_address="addres.of.farmer" -e farmer_port="portnumber"

### or run commands externally with venv (this works for most chia XYZ commands)
docker exec -it chia venv/bin/chia plots add -d /plots

### status from outside the container
docker exec -it chia venv/bin/chia show -s -c

### Connect to testnet?
docker run -d --expose=58444 --expose=8555 -e testnet=true --name <container-name> ghcr.io/chia-network/chia:latest

### Need a wallet?
docker exec -it chia-farmer1 venv/bin/chia wallet show (follow the prompts)




## farmer
sudo mkdir /mnt/md0/chia
sudo mkdir /mnt/md0/chia/plot
sudo mkdir /mnt/md0/chia/keys
sudo chmod 777 /mnt/md0/chia/plot
sudo chmod 777 /mnt/md0/chia/keys

vi /mnt/md0/chia/keys/mnemonic

sudo docker run -d --name chia -p 8555:8555 -p 8444:8444 -e farmer="true"\
    -v /mnt/md0/chia/plot:/plots \
    -v /mnt/md0/chia/keys:/root/.local/share/python_keyring \
    -e keys="/root/.local/share/python_keyring/cryptfile_pass.cfg" \
    --restart=always ghcr.io/chia-network/chia:latest
sudo docker exec -it chia venv/bin/chia keys delete_all
sudo docker exec -it chia venv/bin/chia keys add -f /root/.local/share/python_keyring/mnemonic
sudo docker exec -it chia venv/bin/chia keys show --show-mnemonic-seed
sudo docker exec -it chia venv/bin/chia keys delete -f 

## plotter
sudo mkdir /mnt/md0/chia
sudo mkdir /mnt/md0/chia/plot
sudo chmod 777 /mnt/md0/chia/plot
sudo docker run -d --name chia -e harvester="true" \
    -v /mnt/md0/chia/plot:/plots \
    --restart=always ghcr.io/chia-network/chia:latest

sudo docker exec -it chia venv/bin/chia keys delete_all
sudo docker exec -it chia venv/bin/chia stop all
sudo docker exec -it chia venv/bin/chia stop all -d

sudo docker exec -it chia venv/bin/chia plots create \
    -a 952976454 \
    -f 8beab1d8b6f5d87a4cc15d127726c7b51609e4abcb0a7bfa8f83b7d813ca153815b422d2fe1ffe3531373c4fadb1b12b \
    -p 857192dd57770b02cc83382bad7b0773e611ff8e34ec568f257d2ed062ae237d331d78e8b1f98609ac24e848d6aafdde \
    -t /plots/temp -d /plots -e

## harvester 
sudo mkdir /mnt/md0/chia
sudo mkdir /mnt/md0/chia/plot
sudo mkdir /mnt/md0/chia/ca
sudo mkdir /mnt/md0/chia/mainnet
sudo chmod 777 /mnt/md0/chia/plot
sudo chmod 777 /mnt/md0/chia/ca
sudo chmod 777 /mnt/md0/chia/mainnet

sudo docker run -d --name chia -e harvester="true" \
    -v /mnt/md0/chia/plot:/plots \
    -v /mnt/md0/chia/ca:/root/ca \
    -v /mnt/md0/chia/mainnet:/root/.chia/mainnet \
    --restart=always ghcr.io/chia-network/chia:latest

sudo docker exec -it chia venv/bin/chia stop all -d

sudo docker exec -it chia venv/bin/chia init -c /root/ca
sudo docker exec -it chia vi /root/.chia/mainnet/config/config.yaml
    harvester:
        chia_ssl_ca:
            crt: config/ssl/ca/chia_ca.crt
            key: config/ssl/ca/chia_ca.key
        farmer_peer:
            host: Main.Machine.IP
            port: 8447
sudo docker exec -it chia venv/bin/chia start harvester -r



sudo docker exec -it chia venv/bin/chia plots check -l

sudo docker rm chia -f

sudo docker exec -it chia /bin/bash


