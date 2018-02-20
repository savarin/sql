import abc
import heapq
import Queue
from datetime import datetime as dt


class Node:
    __metaclass__ = abc.ABCMeta

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError


class FileScan(Node):
    def __init__(self, table):
        self.path = table + '.csv'
        self.file = open(self.path, 'r')

        self.rows = self.file.read(4096).split('\r\n')
        self.columns = self.rows.pop(0).split(',')
        self.stub = self.rows.pop()
        self.counter = 0

    def load(self):
        block = self.stub + self.file.read(4096)

        if not block:
            return None

        self.rows = block.split('\r\n')
        self.stub = self.rows.pop()

    def next(self):
        self.counter += 1

        if not self.rows:
            self.load()

        if self.rows:
            row = self.rows.pop(0).split(',')
            return row

        raise StopIteration

    def close(self):
        self.file.close()


class Selection(Node):
    def __init__(self, node, key, value):
        self.node = node
        self.columns = node.columns

        self.index = node.columns.index(key)
        self.value = value

    def next(self):
        while True:
            row = self.node.next()

            if row[self.index] == self.value:
                return row


class Projection(Node):
    def __init__(self, node, columns):
        self.node = node
        self.columns = columns

        self.indices = [node.columns.index(_) for _ in columns]

    def next(self):
        row = self.node.next()
        return [row[_] for _ in self.indices]


class Sort(Node):
    def __init__(self, node, key):
        self.node = node
        self.columns = node.columns

        self.index = node.columns.index(key)
        self.collect = False
        self.queue = Queue.Queue()

    def load(self):
        heap = []

        while True:
            try:
                row = self.node.next()
                heapq.heappush(heap, (row[self.index], row))

            except StopIteration:
                break

        while heap:
            self.queue.put(heapq.heappop(heap)[1])

    def next(self):
        if self.collect:
            if not self.queue.empty():
                return self.queue.get()

            raise StopIteration

        self.collect = True
        self.load()

        return self.queue.get()


class Distinct(Node):
    def __init__(self, node):
        self.node = node
        self.columns = node.columns

        self.prior = None

    def next(self):
        while True:
            row = self.node.next()

            if row != self.prior:
                self.prior = row
                return row


class Aggregate(Node):
    def __init__(self, node):
        self.node = node
        self.columns = node.columns

        self.collect = False
        self.rows = []

    def load(self):
        while True:
            try:
                row = self.node.next()
                self.rows.append(row[0])

            except StopIteration:
                break

    def next(self):
        if not self.collect:
            self.collect = True
            self.load()

        if self.rows:
            result = sum(float(_) for _ in self.rows) / float(len(self.rows))
            self.rows = None
            return result

        raise StopIteration


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


if __name__ == '__main__':
    left = FileScan('mini')
    right = FileScan('movies')

    query = NestedLoopsJoin(Projection(Selection(left,
                                                 'userId', '4'),
                                       ['movieId', 'rating']),
                            Projection(right,
                                       ['movieId', 'title']),
                            'movieId')

    print query.columns

    while True:
        try:
            result = query.next()
            print result

        except StopIteration:
            break

    left.close()
    right.close()
