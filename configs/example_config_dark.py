# This file serves as an example plot config

# Import custom functions (see customfunctions.py)
from customfunctions import *

"""
String: title
The title of the plot
"""
title = 'Example distribution'

"""
String: x_axis_label
Label below the x axis
"""
x_axis_label = 'Percentiles'

"""
String: y_axis_label
Label to the left of the y axis
"""
y_axis_label = 'Y axis label'

"""
float: font_scale
By how much to scale the font (1.0 is normal)
"""
font_scale = 1.2

"""
bool: dark_mode
Whether to use dark background and white text
"""
dark_mode = True

"""
bool: y_log
Whether to print the y axis on a log scale or not
"""
y_log = False

"""
String: file_name
The output plot image filename (directories in the path must already exist otherwise it won't work)
"""
file_name = 'images/example_plot_dark.png'

"""
Int: num_intervals
Amount of intervals to display
0-90, 90-99, 99-99.9, 99.9-99.99 are the first four intervals.
So the more intervals the futher into the nines you go.
Must be at least 1
"""
num_intervals = 4

"""
tuple: (csv filename, column name, optional preprocessing function)
Information that defines a column in a csv file and optionally a preprocessing function that it needs to go through.
The csv should consist of a header in the first line which define column names and data below it
"""
# This is just random data ranging from 1 - 50 (representing millisecond times for example)
source_csv = 'data/example_data.csv'
# And this ranges from 1.000.000 - 100.000.000 (representing nanoseconds times for example)
other_source_csv = 'data/example_data_other.csv'
# Take column1 in the csv file
column1 = (source_csv, 'column1')
column2 = (source_csv, 'column2')
# Here we take the column nanosecond_times but preprocess it first using a custom function (see customfunctions.py)
millisecond_times = (other_source_csv, 'nanosecond_times',
                     convert_nanos_to_millis)

"""
Dict: label_map
Where: Key = label in plot
       Value = tuple of (csv filename, column, and optionally preprocessing function)
"""
label_map = {}
# So column1 will have label 'column 1' in the plot legend
label_map['column 1'] = column1
label_map['column 2'] = column2
label_map['Millisecond times'] = millisecond_times


"""
Dict: combined_columns
Where: Key = label of combined value in plot
       Value = tuple of (combination function, list of tuples of (csv filename, column, and optionally preprocessing function))
Note that the length of the columns in the list MUST be equal in order to properly combine them
"""
combined_columns = {}
# Combine column1 and column2 by summing their elements at the same row, label will be 'column 1+2'
combined_columns['column 1+2'] = (sum, [column1, column2])
# Here we take the max of column1 and the preprocessed nanosecond_times column, label will be 'column max(1,ms)'
combined_columns['column max(1,ms)'] = (max, [column1, column2])
# You can also use custom combination functions (see customfunctions.py)
combined_columns['column avg(1,2)'] = (avg, [column1, column2])


"""
Optional
Dict: label_line
Where: Key = label in plot
       Value = tuple of (marker, line, color) for the given label
If label is left empty/not defined the plotter cycles through all possible options automatically resulting in unique styles.
This is only really needed if you want to group certain lines to seem similar such as having multiple lines of the same marker/linestyle/color.
"""
label_line = {}
# x markers on solid red line
label_line['column 1'] = ('x', '-', 'r')
# triangle down marker on dash-dot red line
label_line['column 2'] = ('v', '-.', 'r')
# plus marker on dashed red line
label_line['column 1+2'] = ('+', '--', 'r')
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
