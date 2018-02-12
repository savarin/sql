import sys


class FileScan(object):
    def __init__(self, table):
        self.path = table + '.csv'
        self.file = open(self.path, 'r')

        data = self.file.read(4096).split('\r\n')
        self.columns = data.pop(0).split(',')
        self.rows = data
        self.stub = data.pop()

    def load(self):
        block = self.stub + self.file.read(4096)

        if not block:
            return None

        self.rows = block.split('\r\n')
        self.stub = data.pop()

    def next(self):
        if not self.rows:
            self.load()

        if self.rows:
            return self.rows.pop()

        sys.stderr.write('EOF reached!\n')
        return None

    def close(self):
        self.file.close()


class Selection(object):
    def __init__(self, filescan):
        self.columns = filescan.columns

    def select(self, data, column, value):
        index = self.columns.index(column)

        result = []
        for row in data:
            if row.split(',')[index] == str(value):
                result.append(row)

        return result


class Projection(object):
    def __init__(self, filescan):
        self.columns = filescan.columns

    def project(self, data, column):
        index = self.columns.index(column)

        result = []
        for row in data:
            result.append(row.split(',')[index])

        return result


class Aggregation(object):
    def __init__(self, filescan):
        pass

    def aggregate(self, data, aggregator):
        if aggregator == 'count':
            return len(data)

        elif aggregator == 'sum':
            return sum(float(_) for _ in data)

        elif aggregator == 'average':
            return sum(float(_) for _ in data) / float(len(data))


if __name__ == '__main__':
    filescan = FileScan('ratings')
    # selection = Selection(filescan)
    # projection = Projection(filescan)
    # aggregation = Aggregation(filescan)
    entries = []

    for i in xrange(10):
        result = filescan.next()

        if not result:
            break

        print result
        # result = selection.select(result, 'movieId', 253)
        # result = projection.project(result, 'rating')
        # entries += result

    # print aggregation.aggregate(entries, 'average')

    filescan.close()
