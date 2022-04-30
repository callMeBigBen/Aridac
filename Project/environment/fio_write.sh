#!/bin/bash

mkdir /test_container
cd /test_container

echo "Randon Write Test..."
fio --name=randwrite --directory=/test_container --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --direct=1 --size="$1"M --rate="$2"k --numjobs="$3" --cmdprio="$4" --runtime=36000 --group_reporting
sleep 10
rm /test_container/randwrite.**

cd ..