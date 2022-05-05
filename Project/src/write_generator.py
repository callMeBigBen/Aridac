# This is a python file that generate fixed amount of disk IO in each second

#!/usr/bin/python
import random
import string


def randStr(chars=string.ascii_uppercase + string.digits, N=200 * 1024):
    return ''.join(random.choice(chars) for _ in range(N))


# Open a file
fo = open("foo.txt", "wb")

fo.write(randStr().encode())

fo.close()
