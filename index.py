

class Node(object):
    def __init__(self, order=2):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def is_full(self):
        return len(self.keys) == self.order

    def find(self, key):
        if self.leaf:
            return self

        for i, item in enumerate(self.keys):
            if key < item:
                return self.values[i].find(key)

        return self.values[i + 1].find(key)

    def split(self):
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order / 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def insert(self, key, value):
        leaf = self.find(key)

        if len(leaf.keys) == 0:
            leaf.keys.append(key)
            leaf.values.append(value)
            return None

        for i, item in enumerate(leaf.keys):
            if key < item:
                leaf.keys = leaf.keys[:i] + [key] + leaf.keys[i:]
                leaf.values = leaf.values[:i] + [value] + leaf.values[i:]
                break

            elif i + 1 == len(leaf.keys):
                leaf.keys.append(key)
                leaf.values.append(value)
                break

        if leaf.is_full():
            leaf.split()

    def show(self, counter=0):
        print counter, str(self.keys), self.leaf

        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)
