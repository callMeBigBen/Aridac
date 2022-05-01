# 1. launch a fio docker A w/ fixed 200kb/s write rate, run for <DP> sec
# 2. launch a fio docker B w/ 15 threads & no-limit write rate
# 3. A will get influenced (if no proper policy)

sudo docker run -dit --rm --device-write-bps /dev/sda:1000000mb --device-read-bps /dev/sda:10mb --mount src=/mnt,target=/test_container,type=bind fio_test:v3 sh -c "./fio_write.sh 10 200 1 1"
sleep 10
sudo docker run -dit --rm --device-write-bps /dev/sda:1000000mb --device-read-bps /dev/sda:10mb --mount src=/mnt,target=/test_container,type=bind fio_test:v3 sh -c "./fio_write.sh 1 10000 15 1"