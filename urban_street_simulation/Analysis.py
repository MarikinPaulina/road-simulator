from tqdm.autonotebook import tqdm
import numpy as np
from scipy.spatial import ckdtree
import shapely
from smallestenclosingcircle import make_circle
import matplotlib.pyplot as plt
from pathlib import Path
import re
import os
from urban_street_simulation.Simulation import load_data


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


def average_segments(path, name):
    regex = fr'*.{name}*.'
    all_files = [file for file in os.listdir(path) if os.path.is_file(file)]
    data_files = [path / file for file in all_files if re.match(regex, file)]
    num_datesets = len(data_files)
    num_segments = 0
    for file in data_files:
        segments = load_data(file)[0]
        num_segments += len(segments)
    return num_segments/num_datesets
