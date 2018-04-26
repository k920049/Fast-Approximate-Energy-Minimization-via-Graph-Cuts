import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import PIL.Image as Image
import sys
import math

from models.solver import Dinic

def file_write(data, file_name):
    if len(data.shape) == 3:
        for channel in range(data.shape[2]):
            f = open(file=file_name + " channel" + str(channel) + ".data", mode="w+")
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    f.write(str(data[i, j, channel]) + " ")
                f.write("\n")
            f.close()
    elif len(data.shape) == 2:
        f = open(file=file_name + ".data", mode="w+")
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                f.write(str(data[i, j]) + " ")
            f.write("\n")
        f.close()
    else:
        print("Not enough dimensions\n")


class GraphCut(object):

    def __init__(self, _iteration, _image, _processed):
        self.iteration = _iteration
        self.image = _image + 16
        self.image_work = _processed + 16

        file_write(self.image, "./resource/image")
        file_write(self.image_work, "./resource/image_work")

        self.size = self.image.size
        self.ngbd = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    def return_mapping_of_image(self, image, alpha, beta):
        # forward pass
        map = {}
        # reverse pass
        revmap = {}

        index = 0
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                # if it contains alpha or beta
                if image[x][y] == alpha or image[x][y] == beta:
                    map[index] = (x, y)
                    revmap[(x, y)] = index
                    index = index + 1

        return map, revmap

    def stationary(self, alpha, beta):
        # retrieve edges
        map, revmap = self.return_mapping_of_image(self.image_work, alpha, beta)
        # initializer solver
        source = len(map)
        sink = len(map) + 1
        solver = Dinic(len(map) + 2)
        solver.set_source_and_sink(source, sink)

        # energy of n-links
        weight = self.Value(alpha, beta)
        # adding n-link edges
        for i in range(len(map)):
            x, y = map[i]
            # searching neighborhood
            for n in self.ngbd:
                if (x + n[0], y + n[1]) in revmap:
                    solver.add_edge(i, revmap[(x + n[0], y + n[1])], weight)

        # add the others
        for i in range(len(map)):
            x, y = map[i]
            cur_ngbd = self.give_ngdb(self.image_work, x, y, alpha, beta)
            # calculate weights
            t_weight_alpha = sum([self.Value(alpha, v) for v in cur_ngbd]) \
                             + self.Data_Value(alpha, self.image, x, y)
            t_weight_beta = sum([self.Value(beta, v) for v in cur_ngbd]) \
                            + self.Data_Value(beta, self.image, x, y)
            if self.image_work[x][y] == alpha:
                solver.add_edge(source, i, t_weight_alpha)
            else:
                solver.add_edge(i, sink, t_weight_beta)

        total_flow = 0
        while solver.bfs():
            solver.clear_work()
            while True:
                flow = solver.dfs(source, sys.maxsize)
                if not flow:
                    break
                total_flow = total_flow + flow

        return total_flow

    def swap(self, alpha, beta):
        # retrieve edges
        map, revmap = self.return_mapping_of_image(self.image_work, alpha, beta)
        # initializer solver
        source = len(map)
        sink = len(map) + 1
        solver = Dinic(len(map) + 2)
        solver.set_source_and_sink(source, sink)
        check = set()
        # getting stationary energy
        # energy = self.stationary(alpha, beta)

        # energy of n-links
        weight = self.Value(alpha, beta)
        # adding n-link edges
        for i in range(len(map)):
            x, y = map[i]
            # searching neighborhood
            for n in self.ngbd:
                if (x + n[0], y + n[1]) in revmap and \
                        (min(i, revmap[(x + n[0], y + n[1])]), max(i, revmap[(x + n[0], y + n[1])])) not in check:
                    check.add((min(i, revmap[(x + n[0], y + n[1])]), max(i, revmap[(x + n[0], y + n[1])])))

                    if self.image_work[x][y] == alpha and \
                            self.image_work[x + n[0]][y + n[1]] == beta:
                        solver.add_edge(i, revmap[(x + n[0], y + n[1])], weight)
                    elif self.image_work[x][y] == beta and \
                            self.image_work[x + n[0]][y + n[1]] == alpha:
                        solver.add_edge(revmap[(x + n[0], y + n[1])], i, weight)
                    else:
                        continue

        # add the others
        for i in range(len(map)):
            x, y = map[i]
            cur_ngbd = self.give_ngdb(self.image_work, x, y, alpha, beta)
            # calculate weights
            t_weight_alpha = sum([self.Value(alpha, v) for v in cur_ngbd])\
                             + self.Data_Value(alpha, self.image, x, y)
            t_weight_beta = sum([self.Value(beta, v) for v in cur_ngbd])\
                            + self.Data_Value(beta, self.image, x, y)
            solver.add_edge(source, i, t_weight_alpha)
            solver.add_edge(i, sink, t_weight_beta)

        total_flow = 0
        while solver.bfs():
            solver.clear_work()
            while True:
                flow = solver.dfs(source, sys.maxsize)
                if not flow:
                    break
                total_flow = total_flow + flow


        res_image = self.image_work
        '''
        print("Total flow: {}, energy: {}".format(total_flow, energy))
        if total_flow < energy:
            S, T = solver.get_cut()
            for i in range(len(map)):
                x, y = map[i]
                if i in S:
                    res_image[x][y] = alpha
                elif i in T:
                    res_image[x][y] = beta
                else:
                    continue
        '''
        edges = solver.get_cut()
        for e in edges:

            if e[0] == source and e[1] == sink:
                continue

            if e[0] == source:
                x, y = map[e[1]]
                res_image[x][y] = alpha
            elif e[1] == sink:
                x, y = map[e[0]]
                res_image[x][y] = beta
            else:
                continue

        return res_image, total_flow

    def solve(self):
        # store all the labels
        label = set()
        # iterate over all the pixels
        for i in range(self.image_work.shape[0]):
            for j in range(self.image_work.shape[1]):
                label.add(self.image_work[i][j])
        # convert the label into numpy array
        labels = []
        for elem in label:
            labels.append(elem)

        for iter in range(self.iteration):
            # iterate over all pairs of labels
            for i in range(len(labels) - 1):
                for j in range(i + 1, len(labels)):
                    self.image_work, flow = self.swap(labels[i], labels[j])
            print("Step: {} -> Energy: {}".format(iter, self.calculate_energy()))

            fig, axes = plt.subplots(ncols=2, figsize=(10, 6))
            axes[0].imshow(self.image,
                           cmap=cm.gray,
                           aspect="equal",
                           interpolation="none",
                           vmin=0.0, vmax=32.0)
            axes[1].imshow(self.image_work,
                           cmap=cm.gray,
                           aspect="equal",
                           interpolation="none",
                           vmin=0.0, vmax=32.0)
            plt.show()


    def calculate_energy(self):
        '''Calculates Energy of image.
           img: is input array'''

        E_data = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                E_data = E_data + self.Data_Value(self.image[i][j], self.image_work, i, j)

        E_smooth = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                n = self.give_neighborhood(self.image_work, i, j)
                E_smooth += sum([self.Value(v, self.image_work[i][j]) for v in n])

        return E_data + E_smooth

    def Value(self, label1, label2):
        return int(abs(label1 - label2))

    def Data_Value(self, label, image, x, y):
        res = abs(label**2 - image[x][y]**2)
        res = math.sqrt(res)
        return int(res)

    def give_neighborhood(self, image, x, y):

        if x < 0 or \
                y < 0 or \
                x >= image.shape[0] or \
                y >= image.shape[1]:
            raise ValueError('Pixel is not in image. x and/or y are to large')

        res = []

        for n in self.ngbd:
            if x + n[0] >= 0 and \
                    y + n[1] >= 0 and \
                    x + n[0] < image.shape[0] and \
                    y + n[1] < image.shape[1]:

                res.append(image[x + n[0]][y + n[1]])
        return res

    def give_ngdb(self, image, x, y, alpha, beta):

        if x < 0 or \
                y < 0 or \
                x >= image.shape[0] or \
                y >= image.shape[1]:
            raise ValueError('Pixel is not in image. x and/or y are to large')

        res = []

        for n in self.ngbd:
            if x + n[0] >= 0 and \
                    y + n[1] >= 0 and \
                    x + n[0] < image.shape[0] and \
                    y + n[1] < image.shape[1]:

                if image[x + n[0]][y + n[1]] == alpha or \
                        image[x + n[0]][y + n[1]] == beta:
                    continue

                res.append(image[x + n[0]][y + n[1]])
        return res
