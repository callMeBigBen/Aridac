from Aridac.Project.src.stats import MAX_DISK_OPS
from limiter import *
from stats import *

ELASTIC = 0.2

def selector(containers, name_to_ratio_i, name_to_ratio_o):
    desired_in = dict()
    desired_out = dict()
    limit_in = dict()
    limit_out = dict()

    idle_ips, idle_ops = MAX_DISK_IPS * pow(1024, 2),  MAX_DISK_OPS * pow(1024, 2)

    for c in containers:
        desired_in[c] = MAX_DISK_IPS * pow(1024, 2) * sum(name_to_ratio_i[c])/len(name_to_ratio_i[c])
        desired_out[c] = MAX_DISK_OPS * pow(1024, 2) * sum(name_to_ratio_o[c])/len(name_to_ratio_o[c])
        limit_in[c] = get_read(c)
        limit_out[c] = get_write(c)

        idle_ips -= limit_in[c]
        idle_ops -= limit_out[c]

        if desired_in[c] * (1+ELASTIC) == limit_in[c]:
            del limit_in[c]
            del desired_in[c]
        if desired_out[c] * (1+ELASTIC) == limit_out[c]:
            del limit_out[c]
            del desired_out[c]

    for c, desire in desired_in.items():
        if desired_in[c] * (1+ELASTIC) > limit_in[c] and idle_ips > 0:
            old_limit = limit_in[c]
            limit_in[c] = min(desired_in[c] * (1+ELASTIC), desired_in[c] + idle_ips)
            idel_ips -= (limit_in[c] - old_limit)
        elif desired_in[c] * (1+ELASTIC) < limit_in[c]:
            idel_ips += (limit_in[c] - desired_in[c] * (1+ELASTIC))
            limit_in[c] = desired_in[c] * (1+ELASTIC)
        else:
            print("No idle bandwidth for Disk Input...")
        set_read(c, limit_in[c])
            
    for c, desire in desired_out.items():
        if desired_out[c] * (1+ELASTIC) > limit_out[c] and idle_ops > 0:
            old_limit = limit_out[c]
            limit_out[c] = min(desired_out[c] * (1+ELASTIC), desired_out[c] + idle_ops)
            idel_ops -= (limit_out[c] - old_limit)
        elif desired_out[c] * (1+ELASTIC) < limit_out[c]:
            idel_ops += (limit_out[c] - desired_out[c] * (1+ELASTIC))
            limit_out[c] = desired_out[c] * (1+ELASTIC)
        else:
            print("No idle bandwidth for Disk Output...")
        set_write(c, limit_out[c])


if __name__ == '__main__':
    






    
    


