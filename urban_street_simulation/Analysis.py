from tqdm.auto import tqdm
import numpy as np
from scipy.spatial import ckdtree
import shapely.geometry
from smallestenclosingcircle import make_circle
from pathlib import Path
import os
from urban_street_simulation.Simulation import load_data
import networkx as nx
import json
import re


def make_polygons(lines, vertices):
    """
    Creates shapely polygons of closed areas based on simulation output.
    It reduces consider segments to important ones - vertices and crossroads,
    finds which ones are connected and uses shapely functions to find areas enclosed in roads.
    Parameters
    ----------
    lines : array_like, shape (N,2,2)
        pares of segments connected in roads
    vertices : array_like

    Returns
    -------
    polygons : list
        shapely polygons of closed areas
    """
    graph = make_graph(lines)
    unique_vertices = find_unique_vertices(graph, vertices)
    new_graph = nx.Graph()
    for vertex in unique_vertices:
        reduce_edges(graph, new_graph, vertex, unique_vertices)
    mp = shapely.geometry.MultiLineString(list(new_graph.edges))
    polygon = mp.buffer(1e-9)
    polygons = [shapely.geometry.Polygon(i) for i in polygon.interiors]
    return polygons


def find_unique_vertices(graph, vertices):
    """
    Takes segments and vertices from simulation output
    and finds set consisting of vertices and crossroads
    Parameters
    ----------
    graph : nx.Graph
        graph with all segments as nodes, and all lines as edges
    vertices : array_like
    Returns
    -------
    unique_vertices : list
        list of coordinates of vertices and crossroads without repetition
    """
    nodes = graph.nodes
    neighbours = [len(list(graph.neighbors(node))) for node in nodes]
    unique_vertices = set(flat_list(vertices))
    unique_vertices |= set(node for i, node in enumerate(nodes) if neighbours[i] != 2)
    return list(unique_vertices)


def make_graph(lines):
    """
    Creates graph with all segments as nodes and all lines as edges
    Parameters
    ----------
    lines : array_like
         pares of segments connected in roads
    Returns
    -------
    graph : nx.Graph
        graph with all segments as nodes and all lines as edges
    """
    graph = nx.Graph()
    for seg1, seg2 in lines:
        graph.add_edge(tuple(seg1), tuple(seg2))
    return graph


def reduce_edges(graph, new_graph, vertex, unique_vertices):
    """
    Reduces edges from given vertex to lines leading to another vertices
    Parameters
    ----------
    graph : nx.Graph
    new_graph : nx.Graph
    vertex : tuple
    unique_vertices : list
    """
    neighbors = list(graph.neighbors(vertex))
    for i in range(len(neighbors)):
        neighbour = neighbors[i]
        old_neighbour = vertex
        while neighbour not in unique_vertices:
            if len(list(graph.neighbors(neighbour))) != 2:
                print(list(graph.neighbors(neighbour)))
                raise IndexError
            new_neighbours = list(graph.neighbors(neighbour))
            new_neighbour = new_neighbours[0] if new_neighbours[0] != old_neighbour else new_neighbours[1]
            if not is_collinear(np.array(old_neighbour), np.array(neighbour), np.array(new_neighbour), 5e-7):
                unique_vertices.append(neighbour)
            else:
                neighbour, old_neighbour = new_neighbour, neighbour
        new_graph.add_edge(vertex, neighbour)


def is_collinear(p1, p2, p3, diff=1e-8):
    v1 = p1 - p2
    v2 = p1 - p3
    return np.isclose(v1[0]*v2[1], v1[1]*v2[0], 0, diff)


def save_polygons(polygons, name):
    """
    Save defining points of shapely polygons to json file with given name
    Parameters
    ----------
    polygons : list
    name : str

    """
    poly_list = [np.array(poly.boundary).tolist() for poly in polygons]
    with open(name, 'w') as file:
        json.dump(poly_list, file)


def load_polygons(name):
    """
    Loads defining points of shapely polygons from json file with given name
    and converts them to list of polygons
    Parameters
    ----------
    name : str

    Returns
    -------
    polygons : list
    """
    with open(name, 'r') as file:
        poly_list = json.load(file)
    polygons = [shapely.geometry.Polygon(i) for i in poly_list]
    return polygons


def roads_vs_centers(path, d=2e-3):

    """
    Calculates average length of roads for simulation with given number of centers.
    returns two lists: numbers of centers and corresponding average roads length.
    Parameters
    ----------
    path: Path

    Returns
    -------
    N : list
        final number of centers for sets of simulations
    L : list
        list of average length of roads for corresponding set of simulation.
    sigma : list
        list of std

    """
    L = []
    N = []
    sigma = []
    for fol in path.iterdir():
        # Ilosc centrów
        N.append(int(re.search('\d+', str(fol).split('/')[-1]).group(0)))
        # liczymy srednią
        l_tab = []
        for file in (fol / 'data').iterdir():
            if re.search('_lines', str(file)):
                l_tab.append(np.load(file).shape[0] * d)
        i = len(l_tab)
        L_sum = sum(l_tab) / i
        L2_sum = sum([x**2 for x in l_tab]) / i
        L.append(L_sum)
        sigma.append((L2_sum-L_sum**2)**0.5)
    return N, L, sigma


def fi_hist(polygons=None, bins=50, path=None, **kwargs):
    """
    Calculates fi factor (the ratio of the area of the polygon to the area of the circumscribed circle)
    for all given polygons and creates its histogram
    Parameters
    ----------
    polygons : list
    bins : int
    path : Path

    Returns
    -------

    """
    polygons = maybe_load_polygons(polygons, path)
    fi = [fi_factor(polygon) for polygon in polygons]

    hist = np.histogram(fi, bins, density=True, **kwargs)
    bins = ((hist[1][:-1] + hist[1][1:]) / 2).tolist()
    hist = (hist[0]).tolist()

    return bins, hist


def maybe_load_polygons(polygons, path):
    if not polygons:
        if path:
            polygons = []
            i = 0
            for file in path.iterdir():
                if re.search('_polygons', str(file)):
                    polygons.extend(load_polygons(file))
                    i += 1
        else:
            raise TypeError
    return polygons


def fi_factor(polygon):
    """
    Calculates fi factor (the ratio of the area of the polygon to the area of the circumscribed circle)
    Parameters
    ----------
    polygon : shapely.geometry.Polygon

    Returns
    -------
    fi : float [0,1]
    """
    circle_points = make_circle(np.array(polygon.boundary.xy).T)
    center = shapely.geometry.Point((circle_points[0], circle_points[1]))
    circle = center.buffer(circle_points[2])
    fi = polygon.area / circle.area
    return fi


def perimeter_hist(N, polygons=None, bins=50, path=None, **kwargs):
    """
    Calculates perimeters of all given polygons and creates modified histogram by:
    - multiplying bins values by square root of final number of centers (N)
    - converting perimeters to they probability, dividing that by square root of N and taking logarithm from it all
    Parameters
    ----------
    N : int
        Number of centers in given simulation
    polygons : list
    bins : int
    path : Path
    kwargs

    Returns
    -------

    """
    polygons = maybe_load_polygons(polygons, path)
    perimeters = [polygon.length for polygon in polygons]

    hist = np.histogram(perimeters, bins, density=True, **kwargs)
    bins = ((hist[1][:-1] + hist[1][1:]) / 2 * N**0.5).tolist()
    hist = (np.log(hist[0] / N**0.5)).tolist()

    # bins = ((hist[1][:-1] + hist[1][1:]) / 2 * N).tolist() # Normalizacja jak w paperze
    return bins, hist


def areas_hist(N, polygons=None, bins=50, path=None, **kwargs):
    """
    Calculates areas of all given polygons and creates modified histogram by:
    - multiplying bins values by final number of centers (N)
    - converting areas to they probability, dividing that by square root of N and taking logarithm from it all
    Parameters
    ----------
    N : int
        Number of centers in given simulation
    polygons : list
    bins : int
    path : Path
    kwargs

    Returns
    ---

    """
    polygons = maybe_load_polygons(polygons, path)
    areas = [polygon.area for polygon in polygons]

    hist = np.histogram(areas, bins, density=True, **kwargs)
    bins = ((hist[1][:-1] + hist[1][1:]) / 2 * N).tolist()
    hist = (np.log(hist[0] / N)).tolist()

    return bins, hist


def flat_list(lista):
    return [tuple(item) for sublist in lista for item in sublist]


def make_circles(polygons):
    return [make_circle(np.array(poly.boundary.xy).T) for poly in polygons]
