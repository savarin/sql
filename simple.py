import sys


class FileScan(object):
    def __init__(self, table):
        self.path = {'movies': 'movies.csv', 'ratings': 'ratings.csv'}
        self.file = open(self.path.get(table), 'r')

        data = self.file.read(4096).split('\r\n')
        self.columns = data.pop(0).split(',')
        self.stub = data
        self.counter = 0        

    def next(self):
        self.counter += 1

        if self.counter == 1:
            result, self.stub = self.stub, ''
            return result

        block = self.stub + self.file.read(4096)

        if not block:
            sys.stderr.write('EOF reached!\n')
            return None

        data = block.split('\r\n')
        self.stub = data.pop()

        return data

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
    selection = Selection(filescan)
    projection = Projection(filescan)
    aggregation = Aggregation(filescan)
    entries = []

    while True:
        result = filescan.next()

        if not result:
            break

        result = selection.select(result, 'movieId', 253)
        result = projection.project(result, 'rating')
        entries += result

    print aggregation.aggregate(entries, 'average')

    filescan.close()
