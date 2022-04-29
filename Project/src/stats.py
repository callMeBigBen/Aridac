# expect to run with root priviledge

import time
import subprocess
import atexit

# 1. probe the maximum throughput for DISK I and O (MB/s)
MAX_DISK_IPS = 185
MAX_DISK_OPS = 40



# 2. start the docker stats as background process and redirect its output
subprocess.Popen(["rm","docker_stats"])
time.sleep(0.5)
stats_log_w = open('docker_stats', 'a+')
server = subprocess.Popen(["docker","stats"], stdout=stats_log_w)


# 3. make sure to kill the child process when the main program exits
def cleanup():
    server.kill() # supported from python 2.6
    print('cleaned up!')
atexit.register(cleanup)


# 4. data structures for stats
name_to_ratio_i = {}
name_to_ratio_o = {}
cur_line = 0
cur_containers = 0
tmp_lines = []

stats_log_r = open('docker_stats', 'a+')
time.sleep(1)
while True:
    # 5. read the docker stats output every given interval
    while not stats_log_r.readline():
        time.sleep(0.2)
    # each loop is new round of output
    while True:
        line = stats_log_r.readline()
        if not line:
            cur_containers = len(tmp_lines)
            break
        tmp_lines.append(tmp_lines, line)
    
    
    # 6. calculate the ratio with new round of input
    for line in tmp_lines:
        elements = line.split()
        block_i = elements[-4]
        block_o = elements[-2]
        container_id = elements[0]
        # process disk input
        if container_id in name_to_ratio_i:
            history_list = name_to_ratio_i[container_id]
            new_ratio_i = float(block_i) / float(MAX_DISK_IPS)
            history_list.append(history_list, new_ratio_i)
            if len(history_list) > 50:
                history_list.pop(0)
        else:
            name_to_ratio_i[container_id] = []
            new_ratio_i = float(block_i) / float(MAX_DISK_IPS)
            history_list.append(history_list, new_ratio_i)
        # process disk output
        if container_id in name_to_ratio_o:
            history_list = name_to_ratio_o[container_id]
            new_ratio_o = float(block_o) / float(MAX_DISK_OPS)
            history_list.append(history_list, new_ratio_o)
            if len(history_list) > 50:
                history_list.pop(0)
        else:
            name_to_ratio_o[container_id] = []
            new_ratio_o = float(block_o) / float(MAX_DISK_OPS)
            history_list.append(history_list, new_ratio_o)
    # 7. pass the ratio map to policy
    