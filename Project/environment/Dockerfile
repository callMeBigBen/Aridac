# FIO container on Ubuntu:latest 
FROM ubuntu:latest 

RUN apt-get update 
RUN apt-get -y install fio wget 
RUN apt-get update && apt-get install fio -y
  
CMD [“/bin/bash”]

# RUN cd /test_container
# RUN fio --name=randread --ioengine=libaio --iodepth=16 --rw=randread --bs=4k --direct=1 --size=256M --numjobs=1 --runtime=36000 --group_reporting
# RUN sleep 10
# RUN rm randread.0.0

# RUN fio --name=randwrite --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --direct=1 --size=256M --numjobs=1 --runtime=36000 --group_reporting
# RUN sleep 10
# RUN rm randwrite.0.0