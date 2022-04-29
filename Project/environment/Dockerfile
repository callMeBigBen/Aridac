# FIO container on Ubuntu:latest 
FROM ubuntu:latest 

# RUN export http_proxy=http://proxy.pdl.cmu.edu:3128/ && export https_proxy=http://proxy.pdl.cmu.edu:3128/
# RUN apt-get update
# RUN apt-get -y install fio wget 
RUN export http_proxy=http://proxy.pdl.cmu.edu:3128/ && export https_proxy=http://proxy.pdl.cmu.edu:3128/ && apt-get update && apt-get install fio -y

# RUN --mount=src=/mnt,target=/test_container,type=bind

COPY fio_test.sh /

COPY fio_read.sh /

COPY fio_write.sh /

# RUN ./fio_test.sh 
  
CMD [“/bin/bash”]
