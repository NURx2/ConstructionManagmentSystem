import itertools
import operator


def sort_uniq(sequence):
    return map(operator.itemgetter(0), itertools.groupby(sorted(sequence)))