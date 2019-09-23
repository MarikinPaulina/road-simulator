import numpy as np
import pytest
from Class_rewrite import Simulation

def test_classLackOfLoopsCentered():
    vertices = [np.array([0,1])]
    segments = [(0,0),(2e-3,0),(-2e-3,0),(2*2e-3,0),(-2*2e-3,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) == 504


def test_classLackOfLoopsSided():
    vertices = [np.array([0,1])]
    segments = [(0,0),(2e-3,0),(2*2e-3,0),(3*2e-3,0),(4*2e-3,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) == 504

def test_classTwoEnds():
    vertices = [np.array([0.5,0])]
    segments = [(0,0),(1,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) == 500

def test_classGCross():
    vertices = [np.array([0.5,0])]
    segments = [(0,0),(1,0),(0.5,0.5),(0.5,-0.5)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) == 1000

def test_classAsymetricLoop():
    vertices = [np.array([0.5,0])]
    segments = [(0,0),(0.75,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) == 375

def test_classBastardVertex():
    vertices = [np.array([0.5,0]), np.array([-0.32,0])]
    segments = [(0,0),(0.75,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) > 375

def test_classUnclosing():
    vertices = [np.array([0.5,0]), np.array([-0.32,0])]
    segments = [(0,0),(0.75,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) > 475

def test_classLoopsVsMulti():   #dwie ścieżki nachodzą na siebie. Nie powoduje błędów
    vertices = [np.array([0.5,0]), np.array([0.2,0])]
    segments = [(0,0),(0.75,0)]
    N = len(vertices); F = 100; M = 10; dN = len(vertices)
    l = 1; d = l*2e-3; epsilon = d*1e-4
    sim = Simulation(N, dN, M, F, l, d, epsilon, test=True, initial_vertices=vertices, initial_segments=segments)
    output = sim.run()
    assert len(output["active_vertices"]) == 0
    assert len(output["segments"]) > 300
