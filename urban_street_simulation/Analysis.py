from tqdm.auto import tqdm
import numpy as np
from scipy.spatial import ckdtree
import shapely
from smallestenclosingcircle import make_circle
from pathlib import Path
import os
from urban_street_simulation.Simulation import load_data
import networkx as nx
import json

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
        if neighbour not in unique_vertices:
            graph.remove_edge(vertex, neighbour)
            while neighbour not in unique_vertices:
                if len(list(graph.neighbors(neighbour))) != 1:
                    print(list(graph.neighbors(neighbour)))
                    raise IndexError
                new_neighbour = list(graph.neighbors(neighbour))[0]
                graph.remove_node(neighbour)
                neighbour = new_neighbour
        new_graph.add_edge(vertex, neighbour)


def save_polygons(polygons, name):
    poly_list = [np.array(poly.boundary).tolist() for poly in polygons]
    with open(name, 'w') as file:
        json.dump(poly_list, file)


def load_polygons(name):
    with open(name, 'r') as file:
        poly_list = json.load(file)
    polygons = [shapely.geometry.Polygon(i) for i in poly_list]
    return polygons


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


def parse_vertices(vertices):
    vertices = set(flat_list(vertices))
    return vertices


def flat_list(lista):
    out = []
    for sublist in lista:
        for item in sublist:
            out.append(tuple(item))
    return out


def make_circles(polygons):
    return [make_circle(np.array(poly.xy).T) for poly in polygons]
