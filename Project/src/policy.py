from limiter import *
from datetime import datetime
import csv

# Configure ELASTIC to your desired value, between 0 through 1
ELASTIC = 0.35

# Quick scale in is more reckless
ENABLE_QUICK_SCALE_IN = False

# Please confirm the MAX_DISK_IPS and MAX_DISK_OPS on your disk before running any test
MAX_DISK_IPS = 2
MAX_DISK_OPS = 1

def selector(containers, name_to_ratio_i, name_to_ratio_o):
    desired_in = dict()
    desired_out = dict()
    limit_in = dict()
    limit_out = dict()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    idle_ips = MAX_DISK_IPS * pow(1024, 2)
    idle_ops = MAX_DISK_OPS * pow(1024, 2)

    # Update limit table for all input containers
    for c in containers:            
        limit_in[c] = get_read(c)
        limit_out[c] = get_write(c)

        idle_ips -= limit_in[c]
        idle_ops -= limit_out[c]

        if len(name_to_ratio_i[c]) > 1:
            desired_in[c] = MAX_DISK_IPS * pow(1024, 2) * sum(name_to_ratio_i[c])/len(name_to_ratio_i[c])

            if desired_in[c] * (1+ELASTIC) == limit_in[c]:
                del desired_in[c]

        if len(name_to_ratio_o[c]) > 1: 
            desired_out[c] = MAX_DISK_OPS * 1024 * 1024 * sum(name_to_ratio_o[c])/len(name_to_ratio_o[c])

            if desired_out[c] * (1+ELASTIC) == limit_out[c]:
                del desired_out[c]

    # Update DISK Input Quota
    for c, desire in desired_in.items():
        if desired_in[c] * (1+ELASTIC) > limit_in[c] and idle_ips > 0:
            old_limit = limit_in[c]
            limit_in[c] = min(desired_in[c] * (1+ELASTIC), desired_in[c] + idle_ips)
            idle_ips -= (limit_in[c] - old_limit)
        elif desired_in[c] * (1+ELASTIC) < limit_in[c] * (1-ELASTIC):
            idle_ips += (limit_in[c] - desired_in[c] * (1+ELASTIC))
            limit_in[c] = desired_in[c] * (1+ELASTIC)
        elif idle_ops <= 0:
            print("No idle bandwidth for Disk Input...")
            if ENABLE_QUICK_SCALE_IN:
                if desired_in[c] * (1+ELASTIC) < limit_in[c] * (1 - pow(ELASTIC, 2)):
                    idle_ips += (limit_in[c] - desired_in[c] * (1+ELASTIC))
                    limit_in[c] = desired_in[c] * (1+ELASTIC)
                    set_read(c, limit_in[c])
            continue
        set_read(c, limit_in[c])
            
    # Update DISK Output Quota
    for c, desire in desired_out.items():
        if desired_out[c] * (1+ELASTIC) > limit_out[c] and idle_ops > 0:
            old_limit = limit_out[c]
            limit_out[c] = min(desired_out[c] * (1+ELASTIC), desired_out[c] + idle_ops)
            idle_ops -= (limit_out[c] - old_limit)
        elif desired_out[c] * (1+ELASTIC) < limit_out[c] * (1-ELASTIC):
            idle_ops += (limit_out[c] - desired_out[c] * (1+ELASTIC))
            limit_out[c] = desired_out[c] * (1+ELASTIC)
        elif idle_ops <= 0:
            print("No idle bandwidth for Disk Output...")
            if ENABLE_QUICK_SCALE_IN:
                if desired_out[c] * (1+ELASTIC) < limit_out[c] * (1 - pow(ELASTIC, 2)):
                    idle_ops += (limit_out[c] - desired_out[c] * (1+ELASTIC))
                    limit_out[c] = desired_out[c] * (1+ELASTIC)
                    set_write(c, limit_out[c])
            continue
        set_write(c, limit_out[c])

    # Write Quota data to csv file
    with open('limit_repeating.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for c in containers:
            spamwriter.writerow([str(current_time)]+ [c] +[str(limit_in[c]/1024)] + [str(limit_out[c]/1024)])

        










    
    


