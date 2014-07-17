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


def graph_data(log_data):
    print(log_data)

    dates_list = []
    eto_values_list = []

    # Organize data
    for date_val in log_data:
        dates_list.append(date_val.date)
    for eto_val in log_data:
        eto_values_list.append(eto_val.eto)
    print(dates_list)
    print(eto_values_list)

    # Draw the graph and render it
    line_chart = pygal.StackedLine(fill=True)
    line_chart.title = 'Evapotranspiration'
    line_chart.x_labels = dates_list
    line_chart.add('Eto', eto_values_list)
    line_chart.render_to_file('chart.svg')

#graph_data(list1)