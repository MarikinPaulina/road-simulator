import numpy as np
from tymczasowa_nazwa.Simulation import RPwC
from tymczasowa_nazwa.Class_rewrite import Simulation


# @pytest.mark.xfail
def test_classStraight():
    vertices = [np.array([0, 1])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0


def test_classDiagonal():
    vertices = [np.array([1, 1])]
    N = len(vertices); M = 10; dN = len(vertices)
    l = 1; d = l*2e-3
    sim = Simulation(N, dN, M, l, d, vertices=vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0


def test_random_mini():
    l = 1; d = l*2e-3
    N = 10; M = 10; dN = 6
    np.random.seed(4)
    vertices = RPwC(l, 4, 0.4)
    sim = Simulation(N, dN, M, l, d, vertices=vertices.T, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 82