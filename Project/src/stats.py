# expect to run with root priviledge

from os import preadv
import time
import subprocess
import atexit
import time

def current_milli_time():
    return float(round(time.time() * 1000))

# 1. probe the maximum throughput for DISK I and O (MB/s)
MAX_DISK_IPS = 2
MAX_DISK_OPS = 1

def cal_iratio(thruput_delta, time_delta):
    return (thruput_delta* (1000.0/time_delta)) / float(MAX_DISK_IPS)

def cal_oratio(thruput_delta, time_delta):
    return (thruput_delta* (1000.0/time_delta)) / float(MAX_DISK_OPS)


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
prev_name_to_i = {}
prev_name_to_o = {}
name_to_ratio_i = {}
name_to_ratio_o = {}
cur_line = 0
cur_containers = 0
tmp_lines = []
# prev_changed_map_i = {}
# prev_changed_map_o = {}
prev_time_map_i = {}
prev_time_map_o = {}

stats_log_r = open('docker_stats', 'a+')
time.sleep(1)
while True:
    prev = current_milli_time()
    # 5. read the docker stats output every given interval
    while not stats_log_r.readline():
        time.sleep(0.1)
    # each loop is new round of output
    now = current_milli_time()
    while True:
        line = stats_log_r.readline()
        if not line:
            break
        tmp_lines.append(line)

    if now == prev: # abandon the transient points
        continue
    
    # 6. calculate the ratio with new round of input
    for line in tmp_lines:
        # print(line)
        elements = line.split()
        if len(elements) < 10 :
            continue
        container_id = elements[0]
        if container_id == "CONTAINER":
            continue
        if  elements[-4].endswith('kB'):
            elements[-4] = elements[-4][:len(elements[-4]) - 2]
            elements[-4] = float(elements[-4]) / 1024.0
        elif  elements[-4].endswith('MB'):
            elements[-4] = elements[-4][:len(elements[-4]) - 2]
        elif  elements[-4].endswith('GB'):
            elements[-4] = elements[-4][:len(elements[-4]) - 2]
            elements[-4] = float(elements[-4]) * 1024.0
        elif  elements[-4].endswith('B'):
            elements[-4] = elements[-4][:len(elements[-4]) - 1]
            elements[-4] = float(elements[-4]) / (1024.0 * 1024.0)
        try:
            acc_block_i = float(elements[-4])
        except ValueError:
            continue
        

        # if  elements[-2].endswith('B'):
        #     elements[-2] = elements[-2][:len(elements[-2]) - 2]
        #     elements[-2] = float(elements[-2]) / 1024.0
        if  elements[-2].endswith('kB'):
            elements[-2] = elements[-2][:len(elements[-2]) - 2]
            elements[-2] = float(elements[-2]) / 1024.0
        elif  elements[-2].endswith('MB'):
            elements[-2] = elements[-2][:len(elements[-2]) - 2]
        elif  elements[-2].endswith('GB'):
            elements[-2] = elements[-2][:len(elements[-2]) - 2]
            elements[-2] = float(elements[-2]) * 1024.0
        elif  elements[-2].endswith('B'):
            elements[-2] = elements[-2][:len(elements[-2]) - 1]
            elements[-2] = float(elements[-2]) / (1024.0 * 1024.0)
        try:
            acc_block_o = float(elements[-2])
        except ValueError:
            continue

        if container_id in prev_name_to_i:
            prev_acc_block_i = prev_name_to_i[container_id]
        else:
            prev_acc_block_i = 0
        block_i = acc_block_i - prev_acc_block_i
        prev_name_to_i[container_id] = acc_block_i

        if container_id in prev_name_to_o:
            prev_acc_block_o = prev_name_to_o[container_id]
        else:
            prev_acc_block_o = 0
        block_o = acc_block_o - prev_acc_block_o
        prev_name_to_o[container_id] = acc_block_o

        # process disk input
        if container_id in name_to_ratio_i:
            history_list = name_to_ratio_i[container_id]
            if container_id in prev_time_map_i:
                new_ratio_i = cal_iratio(block_i, now - prev_time_map_i[container_id])
            else:
                new_ratio_i = cal_iratio(block_i, now - prev)
                prev_time_map_i[container_id] = prev
            if new_ratio_i > 0 and new_ratio_i <= 1:
                history_list.append(new_ratio_i)
            if len(history_list) > 50:
                history_list.pop(0)
        else:
            name_to_ratio_i[container_id] = []
            new_ratio_i = cal_iratio(block_i, now - prev)
            if new_ratio_i > 0 and new_ratio_i <= 1:
                name_to_ratio_i[container_id].append(new_ratio_i)
        # process disk output
        if container_id in name_to_ratio_o:
            history_list = name_to_ratio_o[container_id]
            if container_id in prev_time_map_o:
                new_ratio_o = cal_oratio(block_o, now - prev_time_map_o[container_id])
            else:
                new_ratio_o = cal_oratio(block_o, now - prev)
                prev_time_map_o[container_id] = prev
            if new_ratio_o > 0 and new_ratio_o <= 1:
                history_list.append(new_ratio_o)
            if len(history_list) > 50:
                history_list.pop(0)
        else:
            name_to_ratio_o[container_id] = []
            new_ratio_o = cal_oratio(block_o, now - prev)
            if new_ratio_o > 0 and new_ratio_o <= 1:
                name_to_ratio_o[container_id].append(new_ratio_o)
        if block_o > 0.0:
            prev_time_map_o[container_id] = now
        if block_i > 0.0:
            prev_time_map_i[container_id] = now

    print(name_to_ratio_i)
    print(name_to_ratio_o)
    tmp_lines = []
    # 7. pass the ratio map to policy
    # policy.selector(containers, name_to_ratio_i, name_to_ratio_o)