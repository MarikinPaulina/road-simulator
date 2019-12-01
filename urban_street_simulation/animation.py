from urban_street_simulation.Visual import save_pic, save_pics
from urban_street_simulation.Simulation import RPwC, save_sim
import numpy as np
from urban_street_simulation.Class_rewrite import Simulation
from tqdm.autonotebook import tqdm


# @profile
def main():
    N = 5000
    M = 10
    dN = 6
    l = 1
    d = l*2e-3

    for i in tqdm(range(100)):
        np.random.seed(i*3)

        folder_anim = 'wyniki/wyniki_z_grudnia/n5000_hcor/anim'
        name = f'seed{i*3}'
        folder_data = 'wyniki/wyniki_z_grudnia/n5000_hcor/data'

        array = RPwC(l, 9, 0.5, 0.009)
        sim = Simulation(N, dN, M, l, d, vertices=array.T)
        animation_segments, animation_index, animation_vertices = sim.run()

        save_sim(folder_data, name, (animation_segments, animation_index, animation_vertices))

        s = 0
        tuple_of_arguments = (animation_segments[:animation_index[-1]],
                              animation_vertices[-1], folder_anim, f'{name}.png', None)
        save_pic(tuple_of_arguments)
        # save_pics(animation_segments[s:], animation_index[s:], animation_vertices[s:], folder=folder_anim, name=name)


main()
