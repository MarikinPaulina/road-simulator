from tqdm.autonotebook import tqdm
import numpy as np
from scipy.spatial import ckdtree
import shapely
from smallestenclosingcircle import make_circle
from pathlib import Path
import re
import os
from urban_street_simulation.Simulation import load_data


def areas_hist(polygons, **kwargs):
    areas = np.array([poly.area for poly in polygons])
    return np.histogram(areas, **kwargs)


def perimeters_hist(polygons, **kwargs):
    perimeters = [poly.length for poly in polygons]
    return np.histogram(perimeters, **kwargs)


def circles_hist(polygons, **kwargs):
    areas = np.array([poly.area for poly in polygons])
    circles = make_circles(polygons)
    centers = [shapely.geometry.Point((o[0], o[1])) for o in circles]
    circles_areas = [center.buffer(o[2]) for center, o in zip(centers, circles)]
    return np.histogram(areas/circles_areas, **kwargs)


def make_polygons(lines, d):
    mp = shapely.geometry.MultiLineString(lines.tolist())
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


def average_roads_length(path, name):
    regex = fr'*.{name}*.'
    all_files = [file for file in os.listdir(path) if os.path.is_file(file)]
    data_files = [path / file for file in all_files if re.match(regex, file)]
    num_datesets = len(data_files)
    num_lines = 0
    for file in data_files:
        lines = load_data(file)[0]
        num_lines += len(lines)
    return num_lines/num_datesets


def make_circles(polygons):
    return [make_circle(np.array(poly.xy).T) for poly in polygons]
