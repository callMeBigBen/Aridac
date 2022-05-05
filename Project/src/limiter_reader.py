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
    container_dirs = [f for f in files if not os.path.isfile(f)]
    match_dirs = []
    if d == 'all':
        # list all
        match_dirs = container_dirs
    else:
        # list 1
        match_dirs = [f for f in files if f.startswith(d)]
    return match_dirs


def get_quota(dir):
    path = CONTAINER_BASE_DIR + dir
    print(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True,
                        help='select container, fill in the prefix. Use "all" to adjust all containers\' quota')
    parser.add_argument(
        '-t', required=True, help='r: Get threshold for reading bps\nw: Get threshold for writing bps\n')
    args = parser.parse_args()

    container_dirs = get_containers_dirs(args.d)
    if len(container_dirs) == 0:
        print('no available container found!')
    for container_dir in container_dirs:
        print('-------container update for [%s]-------' % container_dir)

        if args.t == 'r':
            file_path = CONTAINER_BASE_DIR + container_dir + '/' + READ_SUFFIX
            file_content = subprocess.check_output(
                'cat %s' % file_path, shell=True, text=True)
            disk = file_content.split()[0]
            io_before = float(file_content.split()[1])
            print("read: %fmb" % (io_before/1024/1024))
        elif args.t == 'w':
            file_path = CONTAINER_BASE_DIR + container_dir + '/' + WRITE_SUFFIX
            file_content = subprocess.check_output(
                'cat %s' % file_path, shell=True, text=True)
            disk = file_content.split()[0]
            io_before = float(file_content.split()[1])
            print("write: %fmb" % (io_before/1024/1024))
        else:
            print('Invalid argument, please refer to --help.')
            print('r: Get threshold for reading bps\nw: Get threshold for writing bps\n')
