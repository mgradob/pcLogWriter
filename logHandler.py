import datetime

__author__ = 'Miguel'

import os
import shutil

print('abspath: ' + os.path.abspath('logHandler.py'))
print('basename:' + os.path.basename('dataLog.txt'))
print('dirname:' + os.path.dirname(os.path.realpath('logHandler.py')))
print('Exists: ' + str(os.path.exists('Logs')))
print(os.stat(os.path.abspath('dataLog.txt')))

if os.path.exists('Logs'):
#     shutil.move('dataLog.txt', '\Logs')
    print('Logs dir exists')
else:
#     shutil.copy('dataLog.txt', '\Logs\\Up to ' + datetime.datetime.now())
   print('Logs dir does not exists, creating it...')
   os.mkdir(os.path.dirname(os.path.realpath('logHandler.py')) + '\Logs')