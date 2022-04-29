#!/bin/bash

mkdir /test_container
cd /test_container

echo "Randon Read Test..."
fio --name=randread --directory=/test_container --ioengine=libaio --iodepth=16 --rw=randread --bs=4k --direct=1 --size=256M --numjobs=1 --runtime=36000 --group_reporting
sleep 10
rm /test_container/randread.**

echo "Randon Write Test..."
fio --name=randwrite --directory=/test_container --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --direct=1 --size=256M --numjobs=1 --runtime=36000 --group_reporting
sleep 10
rm /test_container/randwrite.**

cd ..
