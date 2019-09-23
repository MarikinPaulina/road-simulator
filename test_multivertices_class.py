import numpy as np
import pytest
from Class_rewrite import Simulation

def test_classTwoToPlay():
    vertices = [np.array([1,1]), np.array([1,-1])]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 102

def test_classCross():
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([1.74,0])]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 102

def test_classSsimultaneous_growing(): #powstają dziwne ścieżki oraz pętle
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([0.5,0.5])]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 91

def test_simultaneous_breach(): #jak wyżej
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([0.45,0.5]), np.array([0.45,-0.5])]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 82
