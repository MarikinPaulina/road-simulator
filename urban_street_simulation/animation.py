from urban_street_simulation.Visual import save_pic, save_pics
from urban_street_simulation.Simulation import RPwC, save_sim
import numpy as np
from urban_street_simulation.Class_rewrite import Simulation


# @profile
def main():
    N = 100
    M = 10
    dN = 6
    l = 1
    d = l*2e-3
    np.random.seed(700)

    folder_anim = 'wyniki/wyniki_z_grudnia/stack/anim'
    name = 'maly'
    folder_data = 'wyniki/wyniki_z_grudnia/stack'

    array = RPwC(l, 7, 0.5, 0.009)
    sim = Simulation(N, dN, M, l, d, vertices=array.T)
    animation_segments, animation_index, animation_vertices = sim.run()

    save_sim(folder_data, name, (animation_segments, animation_index, animation_vertices))

    s = 0
    tuple_of_arguments = (animation_segments[:animation_index[-1]],
                          animation_vertices[-1], folder_anim, 'fin.png', None)
    save_pic(tuple_of_arguments)
    save_pics(animation_segments[s:], animation_index[s:], animation_vertices[s:], folder=folder_anim, name=name)


main()
