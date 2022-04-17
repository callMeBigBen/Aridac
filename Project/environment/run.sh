#!/bin/bash
# docker build -t fio_test:v2 .

sudo docker run -it --device-write-bps /dev/sdb:10mb --device-read-bps /dev/sdb:10mb --mount src=/mnt,target=/test_container,type=bind fio_test:v2 bash


