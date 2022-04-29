#!/bin/bash

# set http & https proxy
export http_proxy=http://proxy.pdl.cmu.edu:3128/
export https_proxy=http://proxy.pdl.cmu.edu:3128/

# change to root
sudo su

# set docker proxy
# https://docs.docker.com/config/daemon/systemd/#httphttps-proxy

apt-get install docker.io || true
docker build -t fio_test:v2 .

docker run -it --device-write-bps /dev/sda:10mb --device-read-bps /dev/sda:10mb --mount src=/users/xuanpeng/,target=/test_container,type=bind fio_test:v2 bash

