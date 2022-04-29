from limiter_reader import *
import argparse
import sys
import os
import subprocess

READ_SUFFIX = 'blkio.throttle.read_bps_device'
WRITE_SUFFIX = 'blkio.throttle.write_bps_device'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True, help='select container, fill in the prefix. Use "all" to adjust all containers\' quota')
    parser.add_argument('-r', type=int, required=False, help='set read mb/s')
    parser.add_argument('-w', type=int, required=False, help='set write mb/s')
    args = parser.parse_args()
    container_dirs = get_containers_dirs(args.d)
    if len(container_dirs) == 0:
        print('no available container found!')
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)
        if args.r:
            file_path = CONTAINER_BASE_DIR + container_dir + '/' + READ_SUFFIX
            file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
            disk = file_content.split()[0]
            io_before = float(file_content.split()[1])
            os.system('echo \"%s %d\" > %s' % (disk, args.r*1024*1024, file_path))
            print("read: %fmb -> %fmb" % (io_before/1024/1024, args.r))
        if args.w:
            file_path = CONTAINER_BASE_DIR + container_dir + '/' + WRITE_SUFFIX
            file_content = subprocess.check_output('cat %s' % file_path, shell=True, text=True)
            disk = file_content.split()[0]
            io_before = float(file_content.split()[1])
            os.system('echo \"%s %d\" > %s' % (disk, args.w*1024*1024, file_path))
            print("write: %fmb -> %fmb" % (io_before/1024/1024, args.w))