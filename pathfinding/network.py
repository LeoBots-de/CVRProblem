"""

{
"graph": {
  "nodes": 3,
  "edges":[[1, 2, 1], [2, 3, 1], [1, 3, 3]]
},
"pickpool":[[3, 5], [2, 4], [4, 3], [3, 9]],
"cap": 10
}


result:
[[2,0],[3],[1]]
"""
from pathfinding.SMatrix import SMatrix
import functools
import multiprocessing
import ctypes


class Network:
    def __init__(self, nodes, edges, picks, cap):
        self.cap = cap
        self.nodes = nodes
        create_storage = functools.partial(
            multiprocessing.RawArray,
            ctypes.c_float
        )
        self.paths = SMatrix(nodes, create_storage)

        for e in edges:
            self.paths[e[0] - 1, e[1] - 1] = e[2]

        self.picks = []

        self.compress_store = [0]
        for pick in picks:
            id = pick[0] - 1
            self.picks.append([id, pick[1]])
            if id not in self.compress_store:
                self.compress_store.append(id)

        self.compress_store.sort()

    def solve(self):
        # print(np.array(self.paths.toarray()))
        self.fill()
        # print(np.array(self.paths.toarray()))
        # self.compress()
        # print(np.array(self.paths.toarray()))
        # sort after further
        items = self.sort_packs(0, [i for i in range(len(self.picks))], True)
        return self.optimize(items)

    def fill(self):
        for i in range(0, self.nodes):
            inodes = self.paths.getrow(i)
            for icoord in range(len(inodes)):
                ival = inodes[icoord]
                if ival != 0:
                    jnodes = self.paths.getrow(icoord) # dict(self.paths.getrow(icoord[1]).todok().items())
                    for jcoord in range(len(jnodes)):
                        if i != jcoord:
                            jval = jnodes[jcoord]
                            if jval != 0:
                                val = ival + jval
                                if self.paths[i, jcoord] == 0 or self.paths[i, jcoord] > val:
                                    self.paths[i, jcoord] = float(val)
                                    # print(f"changed: [{i}, {jcoord}] = {val}")

    def sort_packs(self, origin, packs, furthest = False):
        res = []
        for p in packs:
            pick = self.picks[p]
            load = pick[1]
            node = pick[0]
            way = self.paths[origin, node]
            res.append([node, way, load, p])

        if furthest:
            res.sort(key=lambda k: (k[1], k[2]), reverse=True)
        else:
            res.sort(key=lambda k: (k[1], -k[2]), reverse=False)
        return res


    def compress(self):
        size = len(self.compress_store)
        # print(self.compress_store)
        create_storage = functools.partial(
            multiprocessing.RawArray,
            ctypes.c_float
        )
        compression= SMatrix(size, create_storage)
        for i in range(size):
            for j in range(i+1, size):
                compression[i, j] = self.paths[self.compress_store[i], self.compress_store[j]]

        self.nodes = size
        self.paths = compression

    def calc_trans(self, picks):
        load = 0
        way = 0
        current = 0
        for p in picks:
            pick = self.picks[p]
            load = load + pick[1]
            node = pick[0]
            way = way + self.paths[current, node]
            current = node
        way = way + self.paths[current, 0]

        return load, way

    def optimize(self, items):
        result = []
        while items:
            # start with furthest
            load = items[0][2]
            origin = items[0][0]
            res = [items[0][3]]
            items.remove(items[0])
            full = False
            while not full:
                nitems = [i[3] for i in items]
                closest = self.sort_packs(origin, nitems)
                norigin = -1
                for cnode in closest:
                    if load + cnode[2] > self.cap:
                        continue
                    load = load + cnode[2]
                    norigin = cnode[0]
                    res.append(cnode[3])
                    for i in items:
                        if norigin == i[0]:
                            items.remove(i)
                            break
                    break
                if load == self.cap or norigin == -1:
                    # go home
                    full = True
                else:
                    origin = norigin
            result.append(res)
        return result

    # @staticmethod
    # def test():
    #     network = Network(5, [[1,2,4],[1,3,4],[3,4,5],[1,5,1]], [[3,5],[2,4],[4,3],[3,9]], 10)


# Network.test()
