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
    def selection(column, identifier):
        index = column


if __name__ == '__main__':
    filescan = FileScan('ratings')

    while True:
        result = filescan.next()

        if not result:
            break

    filescan.close()
