import heapq
import Queue

from base import Node
from join import NestedLoopsJoin, HashJoin


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


if __name__ == '__main__':
    left = FileScan('mini')
    right = FileScan('movies')

    query = HashJoin(Projection(Selection(left,
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
