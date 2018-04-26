import numpy as np

class Pair(object):

    def __init__(self):
        self.first = 0
        self.second = 0

    def __init__(self, u, v):
        self.first = u
        self.second = v

    def __lt__(self, other):
        if self.first < other.first:
            return True
        elif self.first == other.first:
            return self.second < other.second
        else:
            return False

    def __le__(self, other):
        if self.first <= other.first:
            return True
        elif self.first == other.first:
            return self.second <= other.second
        else:
            return False

    def __gt__(self, other):
        if self.first > other.first:
            return True
        elif self.first == other.first:
            return self.second > other.second
        else:
            return False

    def __ge__(self, other):
        if self.first >= other.first:
            return True
        elif self.first == other.first:
            return self.second >= other.second
        else:
            return False
