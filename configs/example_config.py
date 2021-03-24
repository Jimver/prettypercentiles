# This file serves as an example plot config

# Import custom functions (see customfunctions.py)
from customfunctions import *

"""
String: title
The title of the plot
"""
title = 'Latency distribution'

"""
String: x_axis_label
Label below the x axis
"""
x_axis_label = 'Percentiles'

"""
String: y_axis_label
Label to the left of the y axis
"""
y_axis_label = 'Latency (ms)'

"""
String: file_name
The plot image filename
"""
file_name = 'images/plot.png'

"""
Int: num_intervals
Amount of intervals to display
For example 0-90, 90-99, 99-99.9, 99.9-99.99 are the first four intervals and so on.
Must be at least 1
"""
num_intervals = 3

"""
String: source_csv
The data source csv filename
The csv should consist of a header in the first line and data below it seperated by commas
"""
source_csv = 'data/example_data.csv'

"""
bool: y_log
Whether to print the y axis on a log scale or not
"""
y_log = False

"""
Dict: column_map
Where: Key = label in plot
       Value = column name in csv OR tuple of column name and pre-processing function that takes a list and outputs a list
"""
column_map = {}
# So column1 in the csv will have 'column 1' as the label in the legend
column_map['column 1'] = 'column1'
column_map['column 2'] = 'column2'
# Here we take the column nanosecond_times but preprocess it first using a custom function (see customfunctions.py)
column_map['Millisecond times'] = ('nanosecond_times', convert_nanos_to_millis)


"""
Dict: combined_columns
Where: Key = label of combined value in plot
       Value = tuple of (combination function, list of column names/tuples of (column name, preprocessing function))
Note that the length of the columns in the list MUST be equal in order to properly combine them
"""
combined_columns = {}
# Combine column1 and column2 by summing their elements at the same row
combined_columns['column 1+2'] = (sum, ['column1', 'column2'])
# Here we take the max of column1 and the preprocessed nanosecond_times column
combined_columns['column max(1,ms)'] = (
    max,
    ['column1', ('nanosecond_times', convert_nanos_to_millis)]
)
# You can also use custom combination functions (see customfunctions.py)
combined_columns['column avg(1,2)'] = (avg, ['column1', 'column2'])


"""
Optional
Dict: label_line
Where: Key = label in plot
       Value = tuple of (marker, line, color) for the given label
If left empty the plotter cycles through all possible options automatically resulting in unique styles.
Only really needed if you want to group certain lines to seem similar such as having multiple lines of the same color.
"""
label_line = {}
# x markers on solid red line
label_line['column 1'] = ('x', '-', 'r')
# triangle down marker on dash-dot cyan line
label_line['column 2'] = ('v', '-.', 'r')
# triangle up marker on dashed blue line
label_line['column max(1,ms)'] = ('^', '--', 'b')
"""
Example values for markers, line types, and colors below, source: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
Markers
character 	description
'.' 	point marker
',' 	pixel marker
'o' 	circle marker
'v' 	triangle_down marker
'^' 	triangle_up marker
'<' 	triangle_left marker
'>' 	triangle_right marker
'1' 	tri_down marker
'2' 	tri_up marker
'3' 	tri_left marker
'4' 	tri_right marker
's' 	square marker
'p' 	pentagon marker
'*' 	star marker
'h' 	hexagon1 marker
'H' 	hexagon2 marker
'+' 	plus marker
'x' 	x marker
'D' 	diamond marker
'd' 	thin_diamond marker
'|' 	vline marker
'_' 	hline marker

Line Styles
character 	description
'-' 	solid line style
'--' 	dashed line style
'-.' 	dash-dot line style
':' 	dotted line style

Colors
The supported color abbreviations are the single letter codes
character 	color
'b' 	blue
'g' 	green
'r' 	red
'c' 	cyan
'm' 	magenta
'y' 	yellow
'k' 	black
'w' 	white
"""
