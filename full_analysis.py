from pathlib import Path
from urban_street_simulation import Analysis as anal
import numpy as np
import matplotlib.pylab as plt
import re
import json
from tqdm.auto import tqdm
from scipy.optimize import curve_fit

input_path = Path('../wyniki/symulacje/ostateczne_wyniki')
output_path = Path('../wyniki/analizy')

N_tab = [300, 600, 1200, 1500]
dist_tab = ['uniform']

def ilosc_centrow_a_dlogosc_drog(dist_path, save_path, dist, d=2e-3):
    r_vs_c = anal.roads_vs_centers(dist_path, d)
    fit = curve_fit(lambda x, a, alpha: a * x **alpha, r_vs_c[0], r_vs_c[1], sigma=r_vs_c[2])
    save = {
        'roadsVScenters': r_vs_c,
        'a': float(fit[0][0]),
        'alpha': float(fit[0][1])
    }
    with open(save_path/f'roadsVScenters.json', 'w') as file:
        json.dump(save, file)
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.errorbar(r_vs_c[0], r_vs_c[1], r_vs_c[2], label='wyniki', fmt='o')
    ax.set_title('Zależność długości dróg od ilości centrów', {'fontsize': 20})
    ax.set_xlabel('N', {'fontsize': 15})
    ax.set_ylabel('L', {'fontsize': 15})
    ax.grid()
    x = np.linspace(min(r_vs_c[0]), max(r_vs_c[0]))
    ax.plot(x, fit[0][0]*x**fit[0][1], label=r'dopasowanie: a N$^{\alpha}$')
    ax.legend(fontsize=15)
    plt.savefig(save_path/f'roadsVScenters_{dist}.png', dpi=300)


def kolowatosc(polygons, save_path, dist, N):
    hist = [anal.fi_hist(poly, 20) for poly in tqdm(polygons)]
    save = {n: h for n, h in zip(N, hist)}
    name = f'fi20_den_{dist}'
    with open(save_path/f'{name}.json', 'w') as file:
        json.dump(save, file)
    fig, ax = plt.subplots(figsize=(16, 12))
    for h, n in zip(hist, N):
        ax.plot(h[0], h[1], 'o', label=f'N = {n}')
    ax.set_title(r'Dystrybucja współczynnika $\phi$', {'fontsize': 20})
    ax.set_xlabel(r'$\phi$', {'fontsize': 15})
    ax.set_ylabel(r'P($\phi$)', {'fontsize': 15})
    ax.grid()
    ax.legend(fontsize=15)
    ax.set_ylim(0)
    plt.savefig(save_path / f'{name}.png', dpi=300)


def obwody(polygons, save_path, dist, N):
    hist = [anal.perimeter_hist(n, poly, 20) for poly, n in zip(polygons, N)]
    save = {n: h for n, h in zip(N, hist)}
    name = f'peri20_den_{dist}'
    with open(save_path/f'{name}.json', 'w') as file:
        json.dump(save, file)
    fig, ax = plt.subplots(figsize=(16, 12))
    for h, n in zip(hist, N):
        ax.plot(h[0], h[1], 'o', label=f'N = {n}')
    ax.set_title(r'Dystrybucja obwodów', {'fontsize': 20})
    ax.set_xlabel(r'p$\sqrt{N}$', {'fontsize': 15})
    ax.set_ylabel(r'ln[P(p)/$\sqrt{N}$]', {'fontsize': 15})
    ax.grid()
    ax.legend(fontsize=15)
    ax.set_xlim(0)
    plt.savefig(save_path / f'{name}.png', dpi=300)


def pola(polygons, save_path, dist, N):
    hist = [anal.areas_hist(n, poly, 20) for poly, n in zip(polygons, N)]
    save = {n: h for n, h in zip(N, hist)}
    name = f'area20_den_{dist}'
    with open(save_path / f'{name}.json', 'w') as file:
        json.dump(save, file)
    fig, ax = plt.subplots(figsize=(16, 12))
    for h, n in zip(hist, N):
        ax.plot(h[0], h[1], 'o', label=f'N = {n}')
    ax.set_title(r'Dystrybucja pól', {'fontsize': 20})
    ax.set_xlabel('aN', {'fontsize': 15})
    ax.set_ylabel(r'ln[P(a)/N]', {'fontsize': 15})
    ax.grid()
    ax.legend(fontsize=15)
    ax.set_xlim(0)
    plt.savefig(save_path / f'{name}.png', dpi=300)


if __name__ == '__main__':
    for dist_path in input_path.iterdir():
        dist = str(dist_path).split('/')[-1]
        # if dist not in dist_tab:
            
        print(dist)
        save_path = output_path/dist
        save_path.mkdir(exist_ok=True)

        # ilosc_centrow_a_dlogosc_drog(dist_path, save_path, dist)
        polygons = []
        N = []
        for n_path in dist_path.iterdir():
            n = int(re.search('\d+', str(n_path).split('/')[-1]).group(0))
            if n not in N_tab:
                N.append(n)
                print(N)
                polygons.append(anal.maybe_load_polygons(None, n_path/'data'))
        # kolowatosc(polygons, save_path, dist, N)
        obwody(polygons, save_path, dist, N)
        pola(polygons, save_path, dist, N)

        # N = []
        # areas = []
        # peris = []
        # for n_path in dist_path.iterdir():
        #     N.append(int(re.search('\d+', str(n_path).split('/')[-1]).group(0)))
        #     polygons = anal.maybe_load_polygons(None, n_path / 'data')
        #     area = []
        #     peri = []
        #     for polys in polygons:
        #         area.append([poly.area for poly in polys])
        #         peri.append([poly.length for poly in polys])
        #     areas.append(area)
        #     peris.append(peri)
        #
        # with open(save_path/f'pola_{dist}.json', 'w') as file:
        #     json.dump({n : a for n, a in zip(N, areas)}, file)
        # with open(save_path / f'obwody_{dist}.json', 'w') as file:
        #     json.dump({n : p for n, p in zip(N, peris)}, file)
