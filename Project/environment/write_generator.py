#!/usr/bin/python
import random
import string
import time

def randStr(chars = string.ascii_uppercase + string.digits, N=200 * 1024):
	return ''.join(random.choice(chars) for _ in range(N))

# Open a file
fo = open("foo.txt", "wb")

for i in range(60):
	fo.write(randStr().encode())
	sleep(0.9)

fo.close()