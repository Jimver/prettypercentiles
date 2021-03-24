def convert_nanos_to_millis(column):
    return [i/1000000 for i in column]


def avg(sequence):
    total = sum(sequence)
    return total/len(sequence)