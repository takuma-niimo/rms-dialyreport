#!/usr/bin/env python3

import subprocess
import datetime
import sys
import time

print('### {0:} getdata_control.py start.'.format(datetime.datetime.now()))

cmd = 'python3 manage.py getdata'

i = 0

while True:
  try:
    subprocess.check_call(cmd.split())
    print('### {0:} (try {1:}) getdata_control.py success.'.format(datetime.datetime.now(), i))
    break

  except:
    print('### {0:} (try {1:}) getdata_control.py failed. start retry.'.format(datetime.datetime.now(), i))
    i += 1
    time.sleep(1800)
    continue

print('### {0:} getdata_control.py end.'.format(datetime.datetime.now()))
