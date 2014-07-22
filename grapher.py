import string

__author__ = 'Miguel'

import pygal
import Logs

# list1 = []
# list1.append(Logs.GraphData(33.33, '2014-06-24 12:00:23.731817'))
# list1.append(Logs.GraphData(32.33, '2014-06-24 12:01:23.731817'))
# list1.append(Logs.GraphData(31.33, '2014-06-24 12:02:23.731817'))
# list1.append(Logs.GraphData(30.33, '2014-06-24 12:03:23.731817'))
# list1.append(Logs.GraphData(29.33, '2014-06-24 12:04:23.731817'))
# list1.append(Logs.GraphData(34.33, '2014-06-24 12:05:23.731817'))
# list1.append(Logs.GraphData(33.33, '2014-06-24 12:06:23.731817'))
# list1.append(Logs.GraphData(38.33, '2014-06-24 12:07:23.731817'))
# list1.append(Logs.GraphData(23.33, '2014-06-24 12:08:23.731817'))


def graph_data(data_list, date_list):
    # Draw the graph and render it
    line_chart = pygal.StackedLine(fill=True)
    line_chart.title = 'Evapotranspiration'
    line_chart.x_labels = date_list
    line_chart.add('Eto', data_list)
    line_chart.render_to_file('chart.svg')
    print('Graph created')


data_arr = []
date_arr = []
file = open('graphDataLog.txt', 'r')
for line in file:
    line_arr = line.split(',')
    data_arr.append(float(line_arr[0]))
    date_arr.append(line_arr[1].rstrip('\n'))

graph_data(data_arr, date_arr)