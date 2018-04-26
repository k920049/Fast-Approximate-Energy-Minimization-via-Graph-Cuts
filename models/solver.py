from asyncio import Queue

class Edge:

    def __init__(self, _v, _cap, _rev):
        self.v = _v
        self.cap = _cap
        self.rev = _rev

class Dinic:

    def __init__(self, _size):
        self.vt = [[] for _ in range(_size)]
        self.vt_copy = [[] for _ in range(_size)]
        self.level = [-1] * _size
        self.work = [0] * _size
        self.size = _size
        self.visited = [False] * self.size

    def set_source_and_sink(self, _S, _E):
        self.S = _S
        self.E = _E

    def clear(self):
        for i in range(self.size):
            self.vt[i].clear()
        self.level = [-1] * self.size
        self.work = [0] * self.size

    def clear_work(self):
        self.work = [0] * self.size

    def add_edge(self, s, e, c):
        #print("Edge added between {} and {}, capacity: {}".format(s, e, c))
        self.vt[s].append(Edge(e, c, len(self.vt[e])))
        self.vt[e].append(Edge(s, 0, len(self.vt[s]) - 1))
        self.vt_copy[s].append(Edge(e, c, len(self.vt[e])))
        self.vt_copy[e].append(Edge(s, 0, len(self.vt[s]) - 1))


    def dfs_cut(self, s):
        self.visited[s] = True
        for i in range(len(self.vt[s])):
            if self.vt[s][i].cap > 0 and not self.visited[self.vt[s][i].v]:
                self.dfs_cut(self.vt[s][i].v)


    def bfs(self):
        self.level = [-1] * self.size
        q = Queue()
        self.level[self.S] = 0;
        #q.put(self.S)
        q.put_nowait(self.S)

        while not q.empty():
            here = q.get_nowait()

            for i in range(len(self.vt[here])):
                there = self.vt[here][i].v
                cap = self.vt[here][i].cap

                if self.level[there] == -1 and cap > 0:
                    self.level[there] = self.level[here] + 1
                    q.put_nowait(there)
        return self.level[self.E] != -1

    def dfs(self, here, crtcap):
        if here == self.E:
            return crtcap

        while True:
            if self.work[here] >= len(self.vt[here]):
                break

            there = self.vt[here][self.work[here]].v
            cap = self.vt[here][self.work[here]].cap

            if self.level[here] + 1 == self.level[there] and cap > 0:
                c = self.dfs(there, min(crtcap, cap))
                if c > 0:
                    self.vt[here][self.work[here]].cap = self.vt[here][self.work[here]].cap - c
                    self.vt[there][self.vt[here][self.work[here]].rev].cap = self.vt[there][self.vt[here][self.work[here]].rev].cap + c
                    return c

            self.work[here] = self.work[here] + 1
        return 0

    def get_cut(self):
        self.dfs_cut(self.S)
        edges = set()
        for here in range(self.size):
            for j in range(len(self.vt[here])):
                there = self.vt[here][j].v
                cap = self.vt_copy[here][j].cap
                if self.visited[here] and not self.visited[there] and cap > 0:
                    edges.add((here, there))
        return edges







