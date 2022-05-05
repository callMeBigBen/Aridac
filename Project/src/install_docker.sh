#!/bin/bash

sudo apt update

echo "sudo apt install apt-transport-https ca-certificates curl software-properties-common"
echo "-------"
echo "Y" || sudo apt install apt-transport-https ca-certificates curl software-properties-common

echo "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"
echo "-------"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

echo "sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable'"
echo "-------"
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

echo "apt-cache policy docker-ce"
echo "-------"
apt-cache policy docker-ce

sleep 3

echo "sudo apt install docker-ce"
echo "-------"
sudo apt install docker-ce || echo "Y"

echo "sudo systemctl status docker"
echo "-------"
sudo systemctl status docker

echo "Configure Docker Proxy"
echo "-------"

sudo mkdir -p /etc/systemd/system/docker.service.d
echo "[Service]" >> /etc/systemd/system/docker.service.d/http-proxy.conf

echo "Environment=\"HTTP_PROXY=http://proxy.pdl.cmu.edu:3128/\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf

echo "Environment=\"HTTPS_PROXY=http://proxy.pdl.cmu.edu:3128/\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf

sudo systemctl daemon-reload
sudo systemctl restart docker
echo "Done..."
