from urban_street_simulation.Visual import save_pic, save_pics
from urban_street_simulation.Simulation import RPwC, save_sim, random_vertex
import numpy as np
from urban_street_simulation.Class_rewrite import Simulation
from tqdm.autonotebook import tqdm


# @profile
def main():
    N_tab = [1000, 500]
    # alpha_tab = [0.5, 2, 0.5, 2, 0.5, 2, 0.5, 2]
    M = 10
    dN = 6
    l = 1
    d = l*2e-3

    for i in tqdm(range(len(N_tab))):
        N = N_tab[i]
        # alpha = alpha_tab[i]
        # cor = 'n' if alpha == 2 else 'h'
        folder_anim = f'wyniki/wyniki_z_grudnia/uniform/n{N}/anim'
        folder_data = f'wyniki/wyniki_z_grudnia/uniform/n{N}/data'

        for j in tqdm(range(100)):
            np.random.seed(j*3)

            name = f'seed{j*3}'

            # array = RPwC(l, 9, alpha, 0.009).T
            array = random_vertex(1, 'uni_square', N)
            sim = Simulation(N, dN, M, l, d, vertices=array)
            animation_segments, animation_index, animation_vertices = sim.run()

            save_sim(folder_data, name, (animation_segments, animation_index, animation_vertices))

            s = 0
            tuple_of_arguments = (animation_segments[:animation_index[-1]],
                                  animation_vertices[-1], folder_anim, f'{name}.png', None)
            save_pic(tuple_of_arguments)
            # save_pics(animation_segments[s:], animation_index[s:], animation_vertices[s:], folder=folder_anim, name=name)


main()
