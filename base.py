import abc


class Node:
    __metaclass__ = abc.ABCMeta

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError
