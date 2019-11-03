import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree
from segcheck import segments_check
import numba.typed
import numba


class Simulation:

    def __init__(self, N=100, dN=1, M=5, l=1, d=2e-3, vertices=None, random_fun=None, test=False,
                 initial_segments=None):
        self.N = N
        self.dN = dN
        self.M = M

        self.l = l
        self.d = d

        self.vertices = vertices

        self.test = test

        self.segments, self.active_vertices, self.animation_vertices, self.animation_segments_index = self._reset()

        if not (initial_segments is None):
            self.segments = initial_segments
        self.random_fun = random_fun
        for i in range(dN):
            new_vertex = self._random_vertex() if vertices is None else vertices[i]
            self.active_vertices.append(new_vertex)

        self.progressbar = tqdm.autonotebook.tqdm(total=self.N)

    def run(self):
        with self.progressbar:
            self.start()
            while len(self.active_vertices) != 0:
                self.one_frame()
            self.fin()
            return self.return_fun()

    def start(self):
        self._find_segments()
        self.N -= len(self.active_vertices)
        self.progressbar.update(self.dN)

    def one_frame(self):
        L = len(self.segments)
        for m in range(self.M):
            self.step()
        if L != len(self.segments):
            self.animation_vertices.append(np.array(self.active_vertices))
            self.animation_segments_index.append(len(self.segments))

    def fin(self):
        self._find_segments()
        self.animation_vertices.append(np.array(self.active_vertices))
        self.animation_segments_index.append(len(self.segments))

    def return_fun(self):
        if self.test:
            return_pack = {
                "active_vertices": self.active_vertices,
                "animation_segments": np.array(self.segments),
                "animation_vertices": self.animation_vertices,
                "animation_segments_index": self.animation_segments_index,
                "segments": self.segments}
            return return_pack
        else:
            return np.array(self.segments), self.animation_segments_index, self.animation_vertices

    def step(self):
        for i in range(len(self.active_segments)-1, -1, -1):
            recalibrate, shuffleB, modified_vertices, i = self._segment_adding(i)
            if shuffleB or recalibrate:
                tree = ckdtree.cKDTree(self.segments)
                if recalibrate:
                    self._find_segments_additive(tree, modified_vertices)
                    break
                if shuffleB:
                    self._shuffle(tree, i)
                    break

    @staticmethod
    def _reset():
        return [(0, 0)], [], [], []

    def _random_vertex(self):
        if self.random_fun == 'pow':
            r = np.random.power(0.5)*self.l
            phi = np.random.random()*2*np.pi
            return np.array([r*np.cos(phi), r*np.sin(phi)])
        elif self.random_fun == 'uni circle':
            r = np.random.random()*self.l
            phi = np.random.random()*2*np.pi
            return np.array([r*np.cos(phi), r*np.sin(phi)])
        elif self.random_fun == 'normal':
            return np.random.normal(0, self.l, size=2)
        elif self.random_fun == 'uni square':
            return np.random.random(size=2)*2*self.l-self.l

    def _find_segments(self):
        self.active_segments = []  # segmenty które będą się rozrastać
        self.segments_vertices = []  # krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
        tree = ckdtree.cKDTree(self.segments)
        for i in range(len(self.active_vertices)-1, -1, -1):
            dist, nearest_segment = tree.query(self.active_vertices[i])
            if dist < self.d:
                if not any(i in lista for lista in self.segments_vertices):
                    self.active_vertices.pop(i)
                    if self.N != 0 and len(self.vertices) > self.dN:
                        new_vertex = self._random_vertex() if self.vertices is None else self.vertices[self.dN]
                        self.dN += 1
                        self.active_vertices.append(new_vertex)
                        self.N -= 1
                        self.progressbar.update(1)

        for i in range(len(self.active_vertices)):
            self._find_segment(i, tree)

    def _find_segment(self, i, tree):
        dist, nearest_segment = tree.query(self.active_vertices[i])
        self.active_vertices[i] = self.active_vertices[i].copy(order='C')
        nearest_segments = tree.query_ball_point(self.active_vertices[i], dist*3)  # TODO: N_jobs
        nearest_segments = self._convert_list_to_typed(nearest_segments)
        segments_check(self.active_vertices[i], nearest_segments, np.array(self.segments))
        for s in nearest_segments:
            if s in self.active_segments:
                index = self.active_segments.index(s)
                if not (i in self.segments_vertices[index]):
                    self.segments_vertices[index].extend([i])
            else:
                self.active_segments.append(s)
                self.segments_vertices.append([i])

    @staticmethod
    def _convert_list_to_typed(L):
        typed_L = numba.typed.List()
        for item in L:
            typed_L.append(item)
        return typed_L

    def _segment_adding(self, i):
        r, r_list, dist_x, dist_y = self._compute_dist(i)
        if r > self.d:
            new_seg = (self.segments[self.active_segments[i]][0]+dist_x,
                       self.segments[self.active_segments[i]][1]+dist_y)
            for j in range(len(r_list)):
                x = self.active_vertices[self.segments_vertices[i][j]][0] - new_seg[0]
                y = self.active_vertices[self.segments_vertices[i][j]][1] - new_seg[1]
                if (x**2+y**2) > r_list[j]**2:
                    break
            else:
                self.segments.append(new_seg)
                self.active_segments[i] = len(self.segments)-1
                return False, False, None, i

        recalibrate, shuffleB, modified_vertices, i = self._recalibration(i, r_list)
        return recalibrate, shuffleB, modified_vertices, i

    def _compute_dist(self, i):
        dist_x = 0
        dist_y = 0
        r_list = []
        for j in range(len(self.segments_vertices[i])):
            x = self.active_vertices[self.segments_vertices[i][j]][0] - self.segments[self.active_segments[i]][0]
            y = self.active_vertices[self.segments_vertices[i][j]][1] - self.segments[self.active_segments[i]][1]
            r = (x**2 + y**2)**0.5
            dist_x += x
            dist_y += y
            r_list.append(r)
        r = (dist_x**2 + dist_y**2)**0.5
        dist_x = dist_x*self.d/r
        dist_y = dist_y*self.d/r
        return r, r_list, dist_x, dist_y

    def _recalibration(self, i, r_list):
        closest_id = np.argmin(r_list)
        vertex = self.segments_vertices[i].pop(closest_id)
        modified_vertices = [vertex]
        shuffleB = True
        if len(self.segments_vertices[i]) == 0:
            self.segments_vertices.pop(i)
            self.active_segments.pop(i)
            i = -1
        else:
            x = self.active_vertices[vertex][0] - self.segments[self.active_segments[i]][0]
            y = self.active_vertices[vertex][1] - self.segments[self.active_segments[i]][1]
            r = r_list[closest_id]
            if r >= self.d:
                new_seg = (self.segments[self.active_segments[i]][0]+x*self.d/r,
                           self.segments[self.active_segments[i]][1]+y*self.d/r)
            else:
                new_seg = (self.active_vertices[vertex][0], self.active_vertices[vertex][1])
            self.segments.append(new_seg)
            self.active_segments.append(len(self.segments)-1)
            self.segments_vertices.append([vertex])
            shuffleB = True
        recalibrate = not any(vertex in lista for lista in self.segments_vertices)
        return recalibrate, shuffleB, modified_vertices, i

    def _shuffle(self, tree, i):
        if i == -1 or len(self.segments) < 2:
            return
        l = len(self.segments) if len(self.segments) < 5 else 5
        dist, potential_segs = tree.query(np.array(self.segments[self.active_segments[i]]), l)
        for v in range(len(self.segments_vertices[i])-1, -1, -1):
            v = self.segments_vertices[i][v]
            dist = []
            for s in potential_segs:
                dist.append((self.active_vertices[v][0] - self.segments[s][0])**2 +
                            (self.active_vertices[v][1] - self.segments[s][1])**2)
            closest = potential_segs[np.argmin(dist)]
            if closest != self.active_segments[i]:
                if not (closest in self.active_segments):
                    self.segments_vertices[i].remove(v)
                    self.active_segments.append(closest)
                    self.segments_vertices.append([v])
                elif v not in self.segments_vertices[self.active_segments.index(closest)]:
                    self.segments_vertices[i].remove(v)
                    index = self.active_segments.index(closest)
                    if v not in self.segments_vertices[index]:
                        self.segments_vertices[index].extend([v])
        if len(self.segments_vertices[i]) == 0:
            self.active_segments.pop(i)
            self.segments_vertices.pop(i)

    def _find_segments_additive(self, tree, modified_vertices):
        for i in range(len(modified_vertices)-1, -1, -1):  # bierzemy teraz modyfikowane wierzchołki
            dist, nearest_segment = tree.query(self.active_vertices[modified_vertices[i]])
            if dist < self.d:
                deleted = modified_vertices[i]
                if not any(deleted in lista for lista in self.segments_vertices):
                    # sprawdzamy czy wszystkie segmenty dotarły do danego wierzchołka
                    if self.N != 0:
                        new_vertex = self._random_vertex() if self.vertices is None else self.vertices[self.dN]
                        self.dN += 1
                        self.active_vertices[deleted] = new_vertex
                        self.N -= 1
                        self.progressbar.update(1)
                    else:
                        modified_vertices.pop(i)
                        self.active_vertices.pop(deleted)
                        self._decrement(modified_vertices, deleted)
                        for lista in self.segments_vertices:
                            self._decrement(lista, deleted)
                else:
                    self._delete(deleted, nearest_segment)

        for i in modified_vertices:
            self._find_segment(i, tree)
        # return N

    @staticmethod
    def _decrement(vertices, deleted):
        for i in range(len(vertices)):
            if vertices[i] > deleted:
                vertices[i] -= 1
            elif vertices[i] == deleted:
                raise ValueError("Multiple instances of vertex in the list")

    def _delete(self, deleted, nearest_segment):
        for i in range(len(self.active_segments)-1, -1, -1):
            if nearest_segment == self.active_segments[i]:
                self.segments_vertices[i].remove(deleted)
                if len(self.segments_vertices[i]) == 0:
                    self.segments_vertices.pop(i)
                    self.active_segments.pop(i)
