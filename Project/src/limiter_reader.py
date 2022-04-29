import math
import os
import sys

def get_quota(path):


if __name__ == '__main__':
    base_dir = '/sys/fs/cgroup/blkio/docker/'
    files = os.listdir(base_dir)
    container_dirs = [ f for f in files if not os.path.isfile(f) ]
    match_dirs = []
    if len(sys.argv) == 0:
        # list all
        match_dirs = container_dirs
    else:
        # list 1
        match_dirs = [ f for f in files if f.startswith(sys.argv) ]
    for d in match_dirs:
        get_quota(d)

