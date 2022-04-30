# start w/ default 10mb r&w quota
sudo docker run -it --rm --device-write-bps /dev/sda:10mb --device-read-bps /dev/sda:10mb --mount src=/mnt,target=/test_container,type=bind fio_test:v3 bash