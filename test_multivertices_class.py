import numpy as np
from Class_rewrite import Simulation


def test_classTwoToPlay():
    vertices = [np.array([1, 1]), np.array([1, -1])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 102


def test_classCross():
    vertices = [np.array([1, 1]), np.array([1, -1]), np.array([1.74, 0])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 102


def test_classSimultaneous_growing(): #powstają dziwne ścieżki oraz pętle
    vertices = [np.array([1, 1]), np.array([1, -1]), np.array([0.5, 0.5])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 91


def test_simultaneous_breach(): #jak wyżej
    vertices = [np.array([1, 1]), np.array([1, -1]), np.array([0.45, 0.5]), np.array([0.45, -0.5])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 82
