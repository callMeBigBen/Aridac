#!/bin/bash
sudo docker build -t fio_test:v2 .

sudo docker run -it --device-write-bps /dev/sda:10mb --device-read-bps /dev/sda:10mb --mount src=/mnt,target=/test_container,type=bind fio_test:v2 bash

