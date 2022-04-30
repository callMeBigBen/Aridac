#!/bin/bash

mkdir /test_container
cd /test_container

echo "Randon Read Test..."
fio --name=randread --directory=/test_container --ioengine=libaio --iodepth=16 --rw=randread --bs=4k --direct=1 --size="$1"M --rate="$2"k --numjobs="$3" --runtime=36000 --group_reporting
sleep 10
rm /test_container/randread.**

cd ..