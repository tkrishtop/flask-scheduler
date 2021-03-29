#!/bin/bash

echo "--------------- Update -----------------------------------------------"
sudo apt-get update

echo "--------------- Docker group setup to run without sudo ---------------"

groupadd --gid 993 docker
usermod -aG docker vagrant

echo "--------------- Docker install ---------------------------------------"

sudo apt-get install docker -y
sudo apt-get install docker-compose -y

echo "--------------- Docker hello world -----------------------------------"

docker run hello-world

echo "--------------- Install pip3 -----------------------------------------"

sudo apt-get update -y
sudo apt-get install python3-pip -y

echo "--------------- Install pytest ---------------------------------------"

pip3 install pytest
export PATH=$PATH:/home/vagrant/.local/bin