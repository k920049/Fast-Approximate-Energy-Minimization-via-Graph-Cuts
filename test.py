def compute_energy(self, u, v, alpha, beta, remain=False):
    sol = Dinic(self.image.size + 8)
    u_x, u_y = self.decode_index(u)
    v_x, v_y = self.decode_index(v)
    color_alpha = self.processed[u_x][u_y]
    color_beta = self.processed[v_x][v_y]
    # initializing solver
    sol.clear()
    sol.set_source_and_sink(_S=self.source, _E=self.sink)
    # Label change
    if not remain:
        temp = alpha
        alpha = beta
        beta = temp
    # adding capacity w.r.t. alpha
    for elem in alpha:
        x, y = self.decode_index(elem)
        # adding capacity from source
        sum = (self.image[x][y] - color_alpha) ** 2
        for d in self.direction:
            ngbd = self.get_index(x + d[0], y + d[1])
            # if a neighbor isn't in P_ab set
            if ngbd == -1 or ngbd in alpha or ngbd in beta:
                continue
            else:
                sum = sum + self.get_energy(color_alpha, self.get_color(ngbd))
        sol.add_edge(s=self.source, e=elem, c=int(sum))
        # adding capacity to sink
        sum = (self.image[x][y] - color_beta) ** 2
        for d in self.direction:
            ngbd = self.get_index(x + d[0], y + d[1])
            # if a neighbor isn't in P_ab set
            if ngbd == -1 or ngbd in alpha or ngbd in beta:
                continue
            else:
                sum = sum + self.get_energy(color_beta, self.get_color(ngbd))
        sol.add_edge(s=elem, e=self.sink, c=int(sum))
    # adding capacity w.r.t. beta
    for elem in beta:
        x, y = self.decode_index(elem)
        # adding capacity from source
        sum = (self.image[x][y] - color_alpha) ** 2
        for d in self.direction:
            ngbd = self.get_index(x + d[0], y + d[1])
            # if a neighbor isn't in P_ab set
            if ngbd == -1 or ngbd in alpha or ngbd in beta:
                continue
            else:
                sum = sum + self.get_energy(color_alpha, self.get_color(ngbd))
        sol.add_edge(s=self.source, e=elem, c=int(sum))
        # adding capacity to sink
        sum = (self.image[x][y] - color_beta) ** 2
        for d in self.direction:
            ngbd = self.get_index(x + d[0], y + d[1])
            # if a neighbor isn't in P_ab set
            if ngbd == -1 or ngbd in alpha or ngbd in beta:
                continue
            else:
                sum = sum + self.get_energy(color_beta, self.get_color(ngbd))
        sol.add_edge(s=elem, e=self.sink, c=int(sum))
    # adding edges between alpha and beta
    for a in alpha:
        for b in beta:
            a_x, a_y = self.decode_index(a)
            b_x, b_y = self.decode_index(b)
            # if they're in neighborhood
            if [a_x - b_x, a_y - b_y] in self.direction:
                energy = self.get_energy(color_alpha, color_beta)
                # print("Energy: {} between color: {}, {}".format(energy, color_alpha, color_beta))
                sol.add_edge(s=a, e=b, c=energy)
    res = 0
    while sol.bfs():
        sol.clear_work()
        while True:
            flow = sol.dfs(self.source, sys.maxsize)
            if not flow:
                break
            res = res + flow

    return res


def solve(self):
    check = set()

    good = False
    count = 0

    print("The number of rooots: {}".format(len(roots)))

    while True:
        good = False
        check.clear()
        for u in roots:
            for v in roots:
                count = count + 1
                # If it's one step away

                if u != v and self.get_color(u) != self.get_color(v) and (min(u, v), max(u, v)) not in check:
                    check.add((min(u, v), max(u, v)))
                    alpha = set()
                    beta = set()
                    alpha.add(u)
                    beta.add(v)
                    # sweep the whole image
                    for k in range(self.image.size):
                        p = find(self.C, k)
                        if p == u:
                            alpha.add(k)
                        if p == v:
                            beta.add(k)
                    energy = self.compute_energy(u=u, v=v, alpha=alpha, beta=beta, remain=True)
                    energy_transposed = self.compute_energy(u=u, v=v, alpha=alpha, beta=beta)

                    print("At step: {} -> Original: {}, Changed: {}".format(count, energy, energy_transposed))
                    # if the energy is smaller than the original
                    if energy_transposed < energy:
                        good = True
                        u_x, u_y = self.decode_index(u)
                        v_x, v_y = self.decode_index(v)
                        temp = self.processed[u_x][u_y]
                        self.processed[u_x][u_y] = self.processed[v_x][v_y]
                        self.processed[v_x][v_y] = temp
                        print("Detected, changing colors from ({}, {}) to ({}, {}".format(u_x, u_y, v_x, v_y))
        if not good:
            break


def get_color(self, u):
    u = find(self.C, u)
    u_x, u_y = self.decode_index(u)
    return self.processed[u_x][u_y]


def get_energy(self, f_p, f_q):
    return int(abs(f_p - f_q))


INF = 987654321
S = 0
E = 25
MAX_A = 60
A = int(ord(u'A'))
a = int(ord(u'a'))
Z = int(ord(u'Z'))
z = int(ord(u'z'))
print("{} {} {} {}".format(A, a, Z, z))

n = int(input())
sol = Dinic(MAX_A)
sol.set_source_and_sink(S, E)

for i in range(n):
    u, v, c = input().split()
    u = int(ord(u))
    v = int(ord(v))
    c = int(c)

    if A <= u and u <= Z:
        u = u - A
    else:
        u = u - a + 26

    if A <= v and v <= Z:
        v = v - A
    else:
        v = v - a + 26

    sol.add_edge(u, v, c)

res = 0
while sol.bfs():
    sol.clear_work()
    while True:
        flow = sol.dfs(S, INF)
        if not flow:
            break
        res = res + flow

print(res)
