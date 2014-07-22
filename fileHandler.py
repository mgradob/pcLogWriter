import os
import datetime

__author__ = 'Miguel'

data_arr = []
if os.path.exists(os.path.abspath('dataLog.txt')):
    try:
        file = open('dataLog.txt')
        for line in file:
            data_arr.append(line)

        with open("C:/Users/Instructor/WA/pcLogWriter/old_files/dataLog_" + str(datetime.date.today()) + ".txt", 'w') as file:
            for line in data_arr:
                file.write(line)

        os.remove('dataLog.txt')
        os.remove('graphDataLog.txt')

    except Exception:
        print('No files found')