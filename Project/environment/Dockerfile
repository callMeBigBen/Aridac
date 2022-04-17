# FIO container on Ubuntu:latest 
FROM ubuntu:latest 

RUN apt-get update 
RUN apt-get -y install fio wget 
RUN apt-get update && apt-get install fio -y

# RUN --mount=src=/mnt,target=/test_container,type=bind

COPY fio_test.sh /

RUN ./fio_test.sh
  
CMD [“/bin/bash”]

