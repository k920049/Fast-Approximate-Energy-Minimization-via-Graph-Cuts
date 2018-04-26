import numpy as np
import math
import sys

from models.solver import Dinic

S = {}
roots = set()

def find(C, u):
    if C[u] != u:
        C[u] = find(C, C[u])
    return C[u]


def union(C, R, u, v, S):

    u = find(C, u)
    v = find(C, v)

    if R[u] > R[v]:
        C[v] = u
        S[v] = S[u] = S[u] + S[v]
        roots.remove(v)
    else:
        C[u] = v
        S[v] = S[u] = S[u] + S[v]
        roots.remove(u)
    if R[u] == R[v]:
        R[v] = R[v] + 1


class Kruskal(object):

    def __init__(self, _image, _min_size, _c):
        self.min_size = _min_size
        self.c = _c
        self.image = _image
        self.sigma = 1.0

        self.direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for i in range(self.image.size):
            roots.add(i)
        self.source = self.image.size + 1
        self.sink = self.image.size + 2
        self.sol = Dinic(self.image.size)

        self.make_matrix()
        self.processed = self.kruskal()

    def print_roots(self):
        for i in roots:
            print("u: {}, parent[u]: {}".format(i, self.C[i]))

    def make_matrix(self):
        total_size = self.image.size

        self.G = {}

        for i in range(total_size):
            self.G[i] = {}

        for u in range(self.image.shape[0]):
            for v in range(self.image.shape[1]):
                i = self.get_index(u, v)

                for d in self.direction:
                    j = self.get_index(u + d[0], v + d[1])

                    if j != -1:
                        self.G[i][j] = self.euclidean(self.image[u][v],
                                                 self.image[u + d[0]][v + d[1]])

    def get_index(self, i, j):

        if i < 0 or i >= self.image.shape[1]:
            return -1

        if j < 0 or j >= self.image.shape[1]:
            return -1

        return i * self.image.shape[1] + j

    def decode_index(self, u):
        x = int(u / self.image.shape[1])
        y = int(u % self.image.shape[1])
        return x, y

    def kruskal(self):

        self.E = [(self.G[u][v], u, v) for u in self.G for v in self.G[u]]
        self.C = {u: u for u in self.G}
        self.R = {u: 0 for u in self.G}
        self.S = {u: 1 for u in range(len(self.G))}
        self.ts = {x: self.threshold(1, self.c) for x in self.C}

        self.E = sorted(self.E)
        T = set()

        for w, u, v in self.E:
            if find(self.C, u) != find(self.C, v):
                if w <= self.ts[u] and w <= self.ts[v]:
                    T.add((u, v))
                    union(self.C, self.R, u, v, self.S)
                    self.ts[u] = w + self.threshold(self.S[u], self.c)

        for _, u, v in self.E:
            if find(self.C, u) != find(self.C, v):
                if self.S[self.C[u]] < self.min_size or self.S[self.C[v]] < self.min_size:
                    union(self.C, self.R, u, v, self.S)

        self.labels = [np.nan for i in range(len(self.C))]
        for i in range(len(self.C)):
            self.labels[i] = int(self.C[i])
        self.T = T

        image = np.zeros_like(self.image)
        for u in range(len(self.labels)):
            i = int(u / self.image.shape[1])
            j = int(u % self.image.shape[1])
            p = find(self.C, self.labels[u])
            p_i = int(p / self.image.shape[1])
            p_j = int(p % self.image.shape[1])

            image[i][j] = self.image[p_i][p_j]
        return image

    def get_color(self, u):
        u = find(self.C, u)
        u_x, u_y = self.decode_index(u)
        return self.processed[u_x][u_y]

    def get_image(self):
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                u = self.get_index(i, j)
                self.processed[i][j] = self.get_color(u)

        return self.processed

    @staticmethod
    def euclidean(x, y):
        return math.sqrt((x - y)**2)

    @staticmethod
    def threshold(size, c):
        return c / size
