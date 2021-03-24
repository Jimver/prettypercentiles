import argparse
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import seaborn as sns
import itertools
import importlib
import sys
from collections import defaultdict
from customfunctions import *


def parse_args(args):
    """
    Parses the arguments of the benchmark plot cli
    Arguments:
        args: Program arguments, excluding first argument (filename being executed)
    Returns: The parsed arguments
    """
    parser = argparse.ArgumentParser(description="prettypercentiles")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="configs.plot_config",
        help="The config file location",
    )
    return parser.parse_args(args)


def combine(func, *arrays):
    """
    Combines n arrays by adding the elements at the same index together in the new array
    Arguments:
        func: function that takes in the n elements at each index and combines them
        *arrays: N arrays to combine
    Returns: A new array where all elements are the combination of the elements at the same index in the source arrays using func
    """
    return [func(elements) for elements in zip(*arrays)]


def get_percentiles(latency_list, percentages):
    """
    Get the percentiles of the given latency list
    Arguments:
        latency_list: The list with latencies as elements
        p: List of percentiles to plot
    Returns: numpy array of the percentiles at the given percentages
    """
    latency_np = np.array(latency_list)  # Convert to numpy array
    sorted_np = np.sort(latency_np)  # Sort latencies

    perc = np.percentile(sorted_np, percentages)
    return perc


def handle_preprocessing(value, columns):
    """
    Calls the nanos to millis and get_percentile function
    Arguments:
        value: Either the column name or tuple of (column name, preprocessing function)
    Returns: If it is just the column name the column as a List, if it is a tuple it will return the preprocessed List of the column
    """
    if isinstance(value, tuple):
        func = value[1]
        column_name = value[0]
        return func(columns[column_name])
    else:
        print(type(value))
        print(value)
        return columns[value]


def main(args):
    """
    Main function, program entrypoint
    Arguments:
        args: The program arguments (excluding first argument which is the file being executed)
    """
    params = parse_args(args)
    config_name = params.config

    # Print config we are using
    print(f'Config: {config_name}')

    # Import config as module
    config = importlib.import_module(config_name)

    # Get plot details
    plot_title = config.title
    x_axis_label = config.x_axis_label
    y_axis_label = config.y_axis_label
    y_log = config.y_log

    # Get number of intervals
    num_intervals = config.num_intervals

    # Get sample points at which to sample intervals
    sample_points = [10.0, 30.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    total_sample_points = sample_points.copy()
    for i in range(1, num_intervals):
        final_point = total_sample_points[-1]
        total_sample_points.extend(
            [final_point + j/(10.0 ** i) for j in sample_points])
    np_sample_points = np.array(total_sample_points)

    # Get file names
    filename = config.file_name
    source_csv = config.source_csv

    # Get line formats
    line_formats = config.label_line

    # Get mappings
    column_map = config.column_map
    combined_columns = config.combined_columns

    # Dict where key = label, value = percentiles
    perc_map = {}

    # each value in each column is appended to a list
    columns = defaultdict(list)

    # Source: https://stackoverflow.com/a/16503661
    with open(source_csv) as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        # read a row as {column1: value1, column2: value2,...}
        for row in reader:
            for (k, v) in row.items():  # go over each column name and value
                # append the value into the appropriate list
                columns[k].append(float(v))
                # based on column name k

    # Individual columns
    for label, value in column_map.items():
        column = handle_preprocessing(value, columns)
        perc_map[label] = get_percentiles(column, np_sample_points)

    # Combined columns
    for label, pair in combined_columns.items():
        # Get list of latencies to combine
        columns_list = [handle_preprocessing(
            value, columns) for value in pair[1]]
        # Combine the latencies and get percentiles
        func = pair[0]
        perc_map[label] = get_percentiles(
            combine(func, *columns_list), np_sample_points)

    # Plot the percentiles
    plot_percentiles_multiple(plot_title, perc_map, np_sample_points, filename,
                              num_intervals, y_log, line_formats, x_axis_label, y_axis_label)

    return


def plot_percentiles_multiple(title, percentiles_map, percentages, filename, num_intervals, y_log, line_formats, x_axis_label, y_axis_label):
    """
    Plot function for the given percentiles
    Adapted from https://stackoverflow.com/questions/42072734/percentile-distribution-graph
    Arguments:
        title: Title of the plot
        percentiles_map: Dict where key is label and value are percentiles
        percentages: The percentages used
        filename: The destination file name of the output image
        num_intervals: The number of intervals to display
        y_log: True will display y axis on log scale, False will use linear scale
        line_formats: Dict where key is label and value is tuple of (marker, linestyle, color) for plot
        x_axis_label: Label below x axis
        y_axis_label: Label to the left of y axis
    """
    # Reset sns before every plot
    sns.reset_defaults()
    clear_bkgd = {'axes.facecolor': 'none', 'figure.facecolor': 'none'}
    sns.set(style='ticks', context='notebook', palette="muted", rc=clear_bkgd)

    x = percentages

    # Number of intervals to display.
    # Later calculations add 2 to this number to pad it to align with the reversed axis
    x_values = 1.0 - 1.0 / 10 ** np.arange(0, num_intervals + 2)

    # Start with hard-coded lengths for 0,90,99
    # Rest of array generated to display correct number of decimal places as precision increases
    lengths = [1, 2, 2] + \
        [int(v) + 1 for v in list(np.arange(3, num_intervals + 2))]

    # Build the label string by trimming on the calculated lengths and appending %
    labels = [str(100 * v)[0:l] + "%" for v, l in zip(x_values, lengths)]

    fig, ax = plt.subplots()
    sns.set(rc={'figure.figsize': (10, 5)})
    # Set x axis to log scale
    ax.set_xscale('log')
    # Invert x axis
    plt.gca().invert_xaxis()
    # Labels have to be reversed because axis is reversed
    ax.xaxis.set_ticklabels(labels[::-1], fontsize=16)

    # Cyclic iteraters for markers and linestyles
    markers = itertools.cycle(['.', ',', 'o', 'v', '^', '<', '>', '1', '2',
                              '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_'])
    linestyles = itertools.cycle(['-', '--', '-.', ':'])

    # Plot distribution with different markers and lines each time
    for key in percentiles_map:
        if key in line_formats:
            marker = line_formats[key][0]
            linestyle = line_formats[key][1]
            color = line_formats[key][2]
            ax.plot([100.0 - v for v in x], percentiles_map[key], marker=marker,
                    linestyle=linestyle, color=color, label=key, alpha=0.7)
        else:
            ax.plot([100.0 - v for v in x], percentiles_map[key], marker=next(markers),
                    linestyle=next(linestyles), label=key, alpha=0.7)

    # Set y labels
    for label in ax.get_yticklabels():
        label.set_fontsize(16)

    # Grid lines
    # Major lines (every 90%, 99%, 99.9%, etc.)
    ax.grid(True, linewidth=0.5, zorder=5)
    ax.grid(True, which='minor', linewidth=0.5,
            linestyle=':')  # Minor lines (10%, 20%,..., 80%, 91%, 92%,...,98%, etc.)

    # Make y axis log scale
    if (y_log):
        ax.set_yscale('log')

    # Set y axis label
    ax.set_ylabel(y_axis_label, fontsize=18)
    # Set x axis label
    ax.set_xlabel(x_axis_label, fontsize=18)
    # Set title
    ax.set_title(title, fontsize=22)

    # Put a legend to the right of the plot
    lg = ax.legend(loc='center left', bbox_to_anchor=(
        1.0, 0.5), fontsize=14)

    sns.despine(fig=fig)

    fig.savefig(filename, dpi=600, bbox_extra_artists=(
        lg,), bbox_inches='tight', format='png')


if __name__ == "__main__":
    main(sys.argv[1:])
