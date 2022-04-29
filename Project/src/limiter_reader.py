import os
import sys

CONTAINER_BASE_DIR = '/sys/fs/cgroup/blkio/docker/'

def get_containers_dirs(argv):
    files = os.listdir(CONTAINER_BASE_DIR)
    container_dirs = [ f for f in files if not os.path.isfile(f) ]
    match_dirs = []
    if len(argv) == 1:
        # list all
        match_dirs = container_dirs
    else:
        # list 1
        match_dirs = [ f for f in files if f.startswith(argv[1]) ]
    return match_dirs

def get_quota(dir):
    path = CONTAINER_BASE_DIR + dir
    print(path)

if __name__ == '__main__':
    match_dirs = get_containers_dirs(sys.argv)
    for d in match_dirs:
        get_quota(d)

