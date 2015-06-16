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

if len(sys.argv) > 1 and sys.argv[1] == 'litian':
    deb_location = sys.argv[2]
    basename = os.path.basename(deb_location)
    os.system('wget {0} -O /tmp/{1}'.format(deb_location, basename))
    log_name = str(time.time())
    sys.exit(os.system('lintian -v /tmp/{0}'.format(basename)))


else:
    if random_num < 50:
        sys.exit(0)
    else:
        sys.exit(1)
