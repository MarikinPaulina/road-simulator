class Simulation:

    def __init__(self, N=100, dN=1, M=5, Frames=10, l=1, d=2e-3, epsilon=2e-7, test=False, initial_vertices=None, initial_segments=None):
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

    def run(self):
        with tqdm.autonotebook.tqdm(total=N) as progressbar:
            while len(active_vertices) != 0:

    def start

    def one_frame

    def step

    def fin


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

    def _random_vertex(self, l):
        return np.random.random(2)*2*l-l
