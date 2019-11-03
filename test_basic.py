import numpy as np
from Simulation import run


def test_straight():
    vertices = [np.array([0, 1])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 51


def test_diagonal():
    vertices = [np.array([1, 1])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments_index"]) == 72
