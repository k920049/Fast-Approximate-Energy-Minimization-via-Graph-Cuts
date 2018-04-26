import numpy as np
import sys

class DisjointSet:

    def __init__(self, n):
        self.parent = [0] * n
        self.rank = [0] * n
        self.cost = [-sys.maxsize] * n
        self.cardinality = [1] * n

        for i in range(n):
            self.parent[i] = i

    def find(self, u):
        if u == self.parent[u]:
            return u
        self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def get_cost(self, u):
        if u == self.parent[u]:
            return self.cost[u]
        return self.get_cost(self.parent[u])

    def get_card(self, u):
        if u == self.parent[u]:
            return self.cardinality[u]
        return self.get_card(self.parent[u])

    def elem(self, u):
        while u != self.parent[u]:
            print(u)
            u = self.parent[u]
        print("u: {}, parent[u]: {}".format(u, self.parent[u]))

    def merge(self, u, v, cost):
        p_u = self.find(u)
        cost_u = self.get_cost(u)
        card_u = self.get_card(u)

        p_v = self.find(v)
        cost_v = self.get_cost(v)
        card_v = self.get_card(v)

        if p_u == p_v:
            return
        if self.rank[p_u] > self.rank[p_v]:
            temp = p_u
            p_u = p_v
            p_v = temp
        self.parent[p_u] = p_v

        cost = max(cost_u, cost)
        cost = max(cost_v, cost)
        self.cost[p_v] = cost

        self.cardinality[p_v] = card_u + card_v

        if self.rank[p_u] == self.rank[p_v]:
            self.rank[p_v] = self.rank[p_v] + 1
