from Simulation import run
import numpy as np
import pytest

def test_twoToPlay():
    vertices = [np.array([1,1]), np.array([1,-1])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 102 #Docierają w różnych (o jeden) czasach przez wypustki. I tak samo wszędzie poniżej

def test_cross():
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([1.74,0])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 102

# @pytest.mark.xfail
def test_simultaneous_growing():
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([0.5,0.5])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 91

def test_simultaneous_breach():
    vertices = [np.array([1,1]), np.array([1,-1]), np.array([0.5,0.5]), np.array([0.5,-0.5])]
    N = len(vertices); F = 100; M = 10
    l = 1; d = l*2e-3; epsilon = d*1e-4
    output = run(N, M, F, l, d, epsilon, test=True, initial_vertices=vertices)
    assert len(output["active_vertices"]) == 0
    assert len(output["animation_segments"]) == 83
