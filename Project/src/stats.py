# expect to run with root priviledge

import time
import subprocess
import atexit
import sys

# 1. probe the maximum throughput for DISK I and O
MAX_DISK_IPS = 0
MAX_DISK_OPS = 0



# start the docker stats as background process and redirect its output
subprocess.Popen(["rm","docker_stats"])
time.sleep(0.5)
stats_log_w = open('docker_stats', 'a+')
server = subprocess.Popen(["docker","stats"], stdout=stats_log_w)


# make sure to kill the child process when the main program exits
def cleanup():
    server.kill() # supported from python 2.6
    print('cleaned up!')
atexit.register(cleanup)


# data structures for stats
name_to_ratio = {}


stats_log_r = open('docker_stats', 'a+')
time.sleep(1)
while True:
    # read the docker stats output every given interval
    while(not stats_log_r.readline()):
        time.sleep(0.1)
    line = stats_log_r.readline()
    elements = line.split()
    if len(elements) != 14:
        print("unexpected output line encounterted. Program abort. Line=:" + line)
        exit(0)

    # calculate the ratio
    

