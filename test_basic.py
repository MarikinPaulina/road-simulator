import numpy as np
from Simulation import run
from Class_rewrite import Simulation
import pytest
def test_straight():
    vertices = [np.array([0,1])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 51

def test_diagonal():
    vertices = [np.array([1,1])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 72

# @pytest.mark.xfail
def test_class():
    N = 10; F = 100; M = 10; dN = 6
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
