#!/usr/bin/python
# -*-coding:utf-8-*-

import sys
import os
import time
import random

random_num = random.randint(0, 100)
print sys.argv[:]
time.sleep(3)
log_handle = open('/home/test/log/{}.log'.format(sys.argv[1]), 'w')

if len(sys.argv) > 1 and sys.argv[2] == 'litian':
    deb_location = sys.argv[3]
    basename = os.path.basename(deb_location)
    os.system('wget {0} -O /tmp/{1}'.format(deb_location, basename))
    log_name = str(time.time())
    sys.exit(os.system('lintian -v /tmp/{0} > /home/test/log/{1}.log'.format(basename, sys.argv[1])))


else:
    if random_num < 50:
        print >> log_handle, random_num, 'pass'
        sys.exit(0)
    else:
        print >> log_handle, random_num, 'fail'
        sys.exit(1)
