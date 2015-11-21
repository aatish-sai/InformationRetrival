"""
Copyright 2015 University of Freiburg
Hannah Bast <bast@cs.uni-freiburg.de>
Evgeny Anatskiy <evgeny.anatskiy@jupiter.uni-freiburg.de>
Numair Mansur <numair.mansur@gmail.com>
"""

import re
import sys

from collections import Counter


class QgramIndex:
    """ A simple q-gram index as explained on the lecture. """

    def __init__(self, q):
        """ Create an empty q-gram index. """

        self.inverted_lists = dict()
        self.q = q

    def read_from_file(self, file_name):
        """
        Construct index from the given file. The format is one record per line.

        >>> qi = QgramIndex(3)
        >>> qi.read_from_file("example.txt")
        >>> sorted(qi.inverted_lists.items())
        [('$$a', [2]), ('$$b', [1]), ('$an', [2]), ('$ba', [1]), ('a$$', [1, \
2]), ('ana', [1, 2]), ('ban', [1]), ('na$', [1, 2])]
        """

        with open(file_name) as file:
            record_id = 0
            for record in file:
                record_id += 1
                record = re.sub("\W+", "", record).lower()
                for qgram in self.qgrams(record):
                    if len(qgram) > 0:
                        # If q-gram is seen for first time, create an empty
                        # inverted list for it. """
                        if qgram not in self.inverted_lists:
                            self.inverted_lists[qgram] = list()
                        self.inverted_lists[qgram].append(record_id)

    def qgrams(self, record):
        """ All q-grams of the given record.

        >>> qi = QgramIndex(3)
        >>> qi.qgrams("bana")
        ['$$b', '$ba', 'ban', 'ana', 'na$', 'a$$']
        """

        qgrams = []
        pad = "$" * (self.q - 1)
        record = pad + record + pad

        for i in range(0, len(record) - self.q + 1):
            qgrams.append(record[i:i + self.q])

        return qgrams

    @staticmethod
    def merge(lists):
        """ Merge the q-gram index lists and return a list of tuples (record_id,
        count).

        >>> QgramIndex.merge([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        [(1, 1), (2, 2), (3, 3), (4, 2), (5, 1)]
        """

        merged_list = list()
        for qgram, l2 in qi.inverted_lists.items():
            l1 = merged_list
            merged_list = list()
            i, j = 0, 0
            while i < len(l1) and j < len(l2):
                if l1[i] < l2[j]:
                    merged_list.append(l1[i])
                    i += 1
                else:
                    merged_list.append(l2[j])
                    j += 1
            if i < len(l1):
                merged_list.extend(l1[i:])
            if j < len(l2):
                merged_list.extend(l2[j:])

        return sorted(Counter(merged_list).most_common())

    @staticmethod
    def compute_ped(p, s):
        """ Compute the prefix edit distance PED(p, s).

        >>> QgramIndex.compute_ped("shwartz", "schwarzenegger")
        2
        """

        # Fake implementation to make the test work, replace by proper code.
        return 2

    def find_matches(self, prefix, delta, k=5, use_qindex=True):
        """ Find all matches for the given prefix with PED at most delta. Return
        the top-k matches.

        use_qindex=True: use the qgram index to produce a list of candidate
        matches, and compute the exact PED only for those (default).

        use_qindex=False: compute the PED for all records (baseline).

        TODO: provide a doctest using the example file or an extension of it.
        """

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 qgram_index.py <file>")
        sys.exit()

    file_name = sys.argv[1]
    qi = QgramIndex(5)
    qi.read_from_file(file_name)

    qi.merge(qi.inverted_lists)

    # for qgram, inverted_list in qi.inverted_lists.items():
    #     print("%s %d" % (qgram, len(inverted_list)))