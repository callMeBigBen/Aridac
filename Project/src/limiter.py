from encodings import search_function
import os
import sys
import argparse
import subprocess

CONTAINER_BASE_DIR = '/sys/fs/cgroup/blkio/docker/'
READ_SUFFIX = 'blkio.throttle.read_bps_device'
WRITE_SUFFIX = 'blkio.throttle.write_bps_device'

def get_containers_dirs(d):
    # d == 'all' or <container-id-prefix>
    files = os.listdir(CONTAINER_BASE_DIR)
    container_dirs = [ f for f in files if not os.path.isfile(f) ]
    match_dirs = []
    if d == 'all':
        # list all
        match_dirs = container_dirs
    else:
        # list 1
        match_dirs = [ f for f in files if f.startswith(d) ]
    return match_dirs

def get_quota(dir):
    path = CONTAINER_BASE_DIR + dir
    print(path)


def get_write(d):
    container_dirs = get_containers_dirs(d)
    if len(container_dirs) == 0:
        print('no available container found!')
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)
        file_path = CONTAINER_BASE_DIR + container_dir + '/' + WRITE_SUFFIX
        file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
        if not file_content:
            return 0
            
        io_before = float(file_content.split()[1])
        print("write: %fmb" % (io_before/1024/1024))
        return io_before

def get_read(d):
    container_dirs = get_containers_dirs(d)
    if len(container_dirs) == 0:
        print('no available container found!')
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)
        file_path = CONTAINER_BASE_DIR + container_dir + '/' + READ_SUFFIX
        file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
        if not file_content:
            return 0

        io_before = float(file_content.split()[1])
        print("read: %fmb" % (io_before/1024/1024))
        return io_before

def set_write(d, new_threshold):
    container_dirs = get_containers_dirs(d)
    if len(container_dirs) == 0:
        print('no available container found!')
    
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)
        file_path = CONTAINER_BASE_DIR + container_dir + '/' + WRITE_SUFFIX
        file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
        disk = file_content.split()[0]
        io_before = float(file_content.split()[1])
        os.system('echo \"%s %d\" > %s' % (disk, new_threshold*1024*1024, file_path))
        print("write: %fmb -> %fmb" % (io_before/1024/1024, new_threshold))

def set_read(d, new_threshold):
    container_dirs = get_containers_dirs(d)
    if len(container_dirs) == 0:
        print('no available container found!')
    
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)
        file_path = CONTAINER_BASE_DIR + container_dir + '/' + READ_SUFFIX
        file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
        disk = file_content.split()[0]
        io_before = float(file_content.split()[1])
        os.system('echo \"%s %d\" > %s' % (disk, new_threshold*1024*1024, file_path))
        print("write: %fmb -> %fmb" % (io_before/1024/1024, new_threshold))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True, help='select container, fill in the prefix. Use "all" to adjust all containers\' quota')
    parser.add_argument('-t', type=str, required=True, help='s: Set new threshold, g: Get current threshold.')
    parser.add_argument('-all', action='store_true', help='Set/Get for both read and write')
    parser.add_argument('-r', action='store_true', help='Set/Get for read')
    parser.add_argument('-w', action='store_true', help='Set/Get for write')
    parser.add_argument('-n', type=int, required=False, help='New threshold in mb/s')
    args = parser.parse_args()


    if args.t == "s":
        if args.n:
            if args.all:
                set_write(args.d, args.n)
                set_read(args.d, args.n)
            elif args.r:
                set_read(args.d, args.n)
            elif args.w:
                set_write(args.d, args.n)
        else:
            print("Missing new threshold, please refer to help.")
    
    if args.t == "g":
        if args.all:
            get_write(args.d)
            get_read(args.d)
        elif args.r:
            get_read(args.d)
        elif args.w:
            get_write(args.d)
        

