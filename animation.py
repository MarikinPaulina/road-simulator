from urban_street_simulation.Visual import save_pic, save_pics
from urban_street_simulation.Simulation import RPwC, save_sim, random_vertex
import numpy as np
from urban_street_simulation.Class_rewrite import Simulation
from tqdm.autonotebook import tqdm


# @profile
def main():
    # N_tab = [5000, 3500, 2000, 1000, 500, 200]
    N_tab = [1500, 1200, 600, 300]
    N_tab = N_tab[::-1]
    M = 10
    dN = 6  
    l = 1
    d = l*2e-3
    alpha = 1.0

    for j in tqdm(range(100)):
        np.random.seed(j*3)

        name = f'seed{j*3}'
        # array = RPwC(l, 9, alpha, 0.009).T
        array = random_vertex(1, 'uni_square', max(N_tab))

        for i in range(len(N_tab)):
            N = N_tab[i]

            folder_anim = f'../wyniki/symulacje/wyniki_z_kwietnia/uniform/n{N}/anim'
            folder_data = f'../wyniki/symulacje/wyniki_z_kwietnia/uniform/n{N}/data'

            sim = Simulation(N, dN, M, l, d, vertices=array)
            animation_segments, animation_index, animation_vertices, lines = sim.run()

            save_dict = {
                'animation_segments': animation_segments,
                'animation_index': animation_index,
                'animation_vertices': animation_vertices,
                'lines': lines
            }
            save_sim(folder_data, name, save_dict)

            # s = 0
            tuple_of_arguments = (animation_segments[:animation_index[-1]],
                                  animation_vertices[-1], folder_anim, f'{name}.png', None)
            save_pic(tuple_of_arguments)


main()
