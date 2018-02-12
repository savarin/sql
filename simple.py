import sys


class FileScan(object):
    def __init__(self, table):
        self.path = {'movies': 'movies.csv', 'ratings': 'ratings.csv'}
        self.file = open(self.path.get(table), 'r')
        self.stub = ''
        self.columns = []
        self.counter = 0

    def next(self):
        block = self.stub + self.file.read(4096)

        if not block:
            sys.stderr.write('EOF reached!\n')
            return None

        data = block.split('\r\n')
        self.stub = data.pop()

        if not self.counter:
            self.columns = data.pop(0).split(',')

        self.counter += 1
        return data

    def close(self):
        self.file.close()


if __name__ == '__main__':
    filescan = FileScan('ratings')

    while True:
        result = filescan.next()

        if not result:
            break

    filescan.close()
