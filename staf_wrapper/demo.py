#!/usr/bin/python
# -*-coding:utf-8-*-

import sys
import os
import time
import random


# while True:
#     time.sleep(20)

random_num = random.randint(0, 100)
print sys.argv[:]
time.sleep(3)


if random_num < 50:
    sys.exit(0)
else:
    sys.exit(1)