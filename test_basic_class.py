import numpy as np
from Simulation import RPwC
from Class_rewrite import Simulation


# @pytest.mark.xfail
def test_classStraight():
    vertices = [np.array([0, 1])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0


def test_classDiagonal():
    vertices = [np.array([1, 1])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0


def test_random_mini():
    l = 1; d = l*2e-3; epsilon = d*1e-4
    N = 10; M = 10; dN = 6
    vertices = RPwC(l, N, 0.4)
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 98