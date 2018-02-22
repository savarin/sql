import collections

from base import Node


class NestedLoopsJoin(Node):
    def __init__(self, left, right, key):
        self.left, self.right = left, right
        self.columns = left.columns + [_ for _ in right.columns if _ != key]

        self.key = key
        self.collect = False
        self.rows = []

    def load(self):
        left_index = self.left.columns.index(self.key)
        right_index = self.right.columns.index(self.key)
        left_rows = []
        right_rows = []

        while True:
            try:
                left_row = self.left.next()
                left_rows.append(left_row)

            except StopIteration:
                break

        while True:
            try:
                right_row = self.right.next()
                right_rows.append(right_row)

            except StopIteration:
                break

        for left_row in left_rows:
            for right_row in right_rows:
                if left_row[left_index] == right_row[right_index]:
                    right_row.pop(right_index)
                    self.rows.append(left_row + right_row)

    def next(self):
        if self.collect:
            if self.rows:
                return self.rows.pop(0)

            raise StopIteration

        self.collect = True
        self.load()

        return self.rows.pop(0)


class HashJoin(Node):
    def __init__(self, left, right, key):
        self.left, self.right = left, right
        self.columns = left.columns + [_ for _ in right.columns if _ != key]

        self.key = key
        self.collect = False
        self.rows = []

    def load(self):
        left_index = self.left.columns.index(self.key)
        right_index = self.right.columns.index(self.key)
        hash_table = collections.defaultdict(list)

        while True:
            try:
                left_row = self.left.next()
                hash_table[hash(left_row[left_index])].append(left_row)

            except StopIteration:
                break

        while True:
            try:
                right_row = self.right.next()

                if hash(right_row[right_index]) in hash_table:
                    for left_row in hash_table[hash(right_row[right_index])]:
                        right_row.pop(right_index)
                        self.rows.append(left_row + right_row)

            except StopIteration:
                break

    def next(self):
        if self.collect:
            if self.rows:
                return self.rows.pop(0)

            raise StopIteration

        self.collect = True
        self.load()

        return self.rows.pop(0)
