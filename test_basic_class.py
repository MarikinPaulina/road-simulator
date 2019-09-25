import numpy as np
from Class_rewrite import Simulation
import pytest

# @pytest.mark.xfail
def test_classStraight():
   vertices = [np.array([0,1])]
   N = len(vertices); F = 100; M = 10; dN = 6
   l = 1; d = l*2e-3; epsilon = d*1e-4
   sim = Simulation(N, dN, M, l, d, epsilon, test=True, initial_vertices=vertices)
   output = sim.run()
   assert len(output["active_vertices"]) == 0

def test_classDiagonal():
   vertices = [np.array([1,1])]
   N = len(vertices); F = 100; M = 10; dN = 6
   l = 1; d = l*2e-3; epsilon = d*1e-4
   sim = Simulation(N, dN, M, l, d, epsilon, test=True, initial_vertices=vertices)
   output = sim.run()
   assert len(output["active_vertices"]) == 0
