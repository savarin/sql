import sys


class FileScan(object):
    def __init__(self, table):
        self.path = {'movies': 'movies.csv', 'ratings': 'ratings.csv'}
        self.file = open(self.path.get(table), 'r')

    def next(self):
        result = self.file.read(4096)

        if not result:
            sys.stderr.write('EOF reached!\n')
            return None

        return result

    def close(self):
        self.file.close()


if __name__ == '__main__':
    filescan = FileScan('ratings')

    while True:
        result = filescan.next()

        try:
            length = len(result)
            print length

        except:
            break

    filescan.close()
