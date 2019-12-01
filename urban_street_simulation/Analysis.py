from tqdm.autonotebook import tqdm
import numpy as np
from scipy.spatial import ckdtree
import shapely


def make_polygons(segments, d):
    mp = shapely.geometry.MultiPoint(segments)
    polygon = mp.buffer(d)
    polygons = [shapely.geometry.Polygon(i) for i in polygon.interiors]
    return polygons


def parse_vertices(vertices):
    vertices = np.unique(np.array(flat_list(vertices)), axis=0)
    return vertices


def flat_list(lista):
    out = []
    for sublist in lista:
        for item in sublist:
            out.append(item)
    return out
