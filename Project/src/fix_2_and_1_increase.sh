# 1. launch a fio docker A & B w/ fixed 10MB/s write rate, run for <DP> sec
# 2. increase a fio docker B w/ no-limit write rate
# 3. A will get influenced (if no proper policy)

sudo docker run -dit --rm --device-write-bps /dev/sda:1000000mb --device-read-bps /dev/sda:1000000mb --mount src=/mnt,target=/test_container,type=bind fio_test:v3 sh -c "./fio_write.sh 512 200 1 1" &
sudo docker run -dit --rm --device-write-bps /dev/sda:1000000mb --device-read-bps /dev/sda:1000000mb --mount src=/mnt,target=/test_container,type=bind fio_test:v3 sh -c "./increase_disk.sh" &