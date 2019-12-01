import numpy as np
from urban_street_simulation.Class_rewrite import Simulation


def test_random10():
    N = 10; M = 10; dN = 6
    l = 1; d = l*2e-3
    np.random.seed(4)
    sim = Simulation(N, dN, M, l, d, random_fun='uni square', test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 108

def test_randomNorm():
    N = 10; M = 10; dN = 6
    l = 1; d = l*2e-3
    np.random.seed(7)
    sim = Simulation(N, dN, M, l, d, random_fun='normal', test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 98

def test_random10Table():
    N = 10; M = 10; dN = 6
    l = 1; d = l*2e-3
    np.random.seed(4)
    vertices = np.random.random(size=(N,2))*2*l-l
    sim = Simulation(N, dN, M, l, d, vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 108

def test_randomNormTable():
    N = 10; M = 10; dN = 6
    l = 1; d = l*2e-3
    np.random.seed(7)
    vertices = np.random.normal(0,l,size=(N,2))
    sim = Simulation(N, dN, M, l, d, vertices, test=True)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_vertices"]) == 98
