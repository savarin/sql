import os
import sys
import time
from datetime import datetime as dt


class FileScan(object):
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
            return self.rows.pop().split(',')

        sys.stderr.write(str(dt.now()) + ' WARN EOF reached!\n')
        return None

    def close(self):
        self.file.close()


class Selection(object):
    def __init__(self, filescan, column, value):
        self.index = filescan.columns.index(column)
        self.value = value

    def map(self, row):
        if row and int(row[self.index]) == self.value:
            return row


class Projection(object):
    def __init__(self, filescan, columns):
        self.indices = [filescan.columns.index(column) for column in columns]

    def map(self, row):
        if row:
            return [row[index] for index in self.indices]


class Aggregation(object):
    def __init__(self, filescan, aggregator):
        self.aggregator = aggregator

    def reduce(self, results):
        if self.aggregator == 'count':
            return len(results)

        elif self.aggregator == 'sum':
            return sum(float(_) for _ in results)

        elif self.aggregator == 'average':
            return sum(float(_) for _ in results) / float(len(results))


if __name__ == '__main__':
    filescan = FileScan('ratings')
    selection = Selection(filescan, 'movieId', 3)
    projection = Projection(filescan, ['rating'])
    aggregation = Aggregation(filescan, 'average')
    results = []

    while True:
        result = filescan.next()

        if not result:
            break

        if os.getenv('SQL_DEBUG') and not filescan.counter % 1000000:
            counter = filescan.counter / 1000000
            sys.stderr.write(str(dt.now()) + ' INFO ' + str(counter) + ' mm rows\n')

        result = selection.map(result)
        result = projection.map(result)

        if result:
            results += result

    print aggregation.reduce(results)

    filescan.close()
