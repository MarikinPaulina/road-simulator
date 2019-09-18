import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree
from segcheck import segments_check
import numba.typed, numba

class Simulation:

    def __init__(self, N=100, dN=1, M=5, Frames=10, l=1, d=2e-3, epsilon=2e-7, random_fun=None, test=False, initial_vertices=None, initial_segments=None):
        self.N = N
        self.dN = dN
        self.M = M
        self.Frames = Frames

        self.l = l
        self.d = d
        self.epsilon = epsilon


        self.test = test

        self.segments, self.active_vertices, self.animation_vertices, self.animation_segments = self._reset()

        if not (initial_segments is None):
            self.segments = initial_segments
        self.random_fun = 'homo_square' if random_fun is None else random_fun
        if initial_vertices is None:
            for i in range(dN):
                new_vertex = self._random_vertex()
                self.active_vertices.append(new_vertex)
        else:
            self.active_vertices = initial_vertices



    def run(self):
        with tqdm.autonotebook.tqdm(total=self.N) as self.progressbar:
            self.start()
            while len(active_vertices) != 0:
                self.one_frame()
            self.fin()
            return self.return_run()

    def start(self):
        N_new = _find_segments(self.N - len(self.active_vertices))
        Ndelta, self.N = self.N - N_new, N_new
        self.progressbar.update(Ndelta)


    def one_frame():
        L = len(self.segments)
        for m in range(self.M):
            N_new = step()
            # N_new = _segments_adding()
        Ndelta, self.N = self.N - N_new, N_new
        self.progressbar.update(Ndelta)
        if L != len(self.segments):
            self.animation_vertices.append(np.array(self.active_vertices))
            self.animation_segments.append(np.array(self.segments))


    def fin(self):
        self.N = _find_segments(self.N)
        Ndelta, self.N = self.N - N_new, N_new
        self.progressbar.update(Ndelta)
        self.animation_vertices.append(np.array(self.active_vertices))
        self.animation_segments.append(np.array(self.segments))


    def return_run(self):
            if self.test:
                return_pack = {
                "active_vertices" : self.active_vertices,
                "animation_segments" : self.animation_segments,
                "animation_vertices" : self.animation_vertices,
                "segments" : self.segments}
                return return_pack
            else:
                return [self.animation_segments,self.animation_vertices]

    def step(self):
        # recalibrate = False
        for i in range(len(self.active_segments)-1, -1, -1):
            recalibrate, shuffleB, modified_vertices, i = _segment_adding(i, )#recalibrate)
            if shuffleB or recalibrate:
                tree = ckdtree.cKDTree(self.segments)
                if recalibrate:
                    N = _find_segments_additive(tree, modified_vertices)
                    recalibrate = False
                    break
                if shuffleB:
                    shuffle(tree, i)
                    shuffleB = False
                    break
        return N


    def reset(self, N=100, dN=1, M=5, Frames=10, l=1, d=2e-3, epsilon=2e-7, test=False, initial_vertices=None, initial_segments=None):
        self.N = N
        self.dN = dN
        self.M = M
        self.Frames = Frames

        self.l = l
        self.d = d
        self.epsilon = epsilon

        self.test = test

        self.segments, self.active_vertices, self.animation_vertices, self.animation_segments = _reset()

        if not (initial_segments is None):
            self.segments = initial_segments
        if initial_vertices is None:
            for i in range(number_of_vertices):
                new_vertex = _random_vertex(l)
                self.active_vertices.append(new_vertex)
        else:
            self.active_vertices = initial_vertices
        self.N -= len(self.active_vertices)

    def _reset(self):
        return [(0,0)], [], [], []

    def _random_vertex(self):
        if self.random_fun == 'homo square':
            return np.random.random(2)*2*self.l-self.l
        elif self.random_fun == 'homo circle':
            r = np.random.random()*self.l
            phi = np.random.random()*2*np.pi
            return np.array([r*np.cos(phi),r*np.sin(phi)])
        elif self.random_fun == 'normal':
            return np.random.normal(0,self.l,size=2)

    def _find_segments(self,N):
        self.active_segments = [] #segmenty które będą się rozrastać
        self.segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
        tree = ckdtree.cKDTree(segments)
        for i in range(len(self.active_vertices)-1,-1,-1):
            dist, nearest_segment = tree.query(self.active_vertices[i])
            if dist < self.d:
                if not any(i in lista for lista in self.segments_vertices):
                    self.active_vertices.pop(i)
                    if N != 0:
                        new_vertex = self._random_vertex()
                        self.active_vertices.append(new_vertex)
                        N -= 1
        for i in range(len(self.active_vertices)):
