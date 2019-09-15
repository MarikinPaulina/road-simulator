import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree
from segcheck import segments_check
import numba.typed, numba

def run(N,M,Frames,l,d,epsilon, number_of_vertices = 1, test=False, initial_vertices = None, initial_segments=None):
    segments, active_vertices, animation_vertices, animation_segments = reset()
    if not (initial_segments is None):
        segments = initial_segments
    if initial_vertices is None:
        for i in range(number_of_vertices):
            new_vertex = random_vertex(l)
            active_vertices.append(new_vertex)
    else:
        active_vertices = initial_vertices
    N -= len(active_vertices)

    with tqdm.autonotebook.tqdm(total=N) as progressbar:
        while len(active_vertices) != 0:
            active_segments, segments_vertices, N_new = find_segments(active_vertices, segments,d,epsilon,l, N)
            Ndelta, N = N - N_new, N_new
            progressbar.update(Ndelta)
            for f in range(Frames):
                L = len(segments)
                active_segments, segments_vertices, N_new = segments_adding(M,active_vertices,active_segments,segments_vertices,segments,d,epsilon, l, N)
                Ndelta, N = N - N_new, N_new
                progressbar.update(Ndelta)
                if L != len(segments):
                    animation_vertices.append(np.array(active_vertices))
                    animation_segments.append(np.array(segments))

    active_segments, segments_vertices, N = find_segments(active_vertices, segments,d,epsilon, l, N)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))

    if test:
        return_pack = {
        "active_vertices" : active_vertices,
        "animation_segments" : animation_segments,
        "animation_vertices" : animation_vertices,
        "segments" : segments}
        return return_pack
    else:
        segments = np.vstack(np.array(segments)).T
        return [animation_segments,animation_vertices]

def reset():
    return [(0,0)], [], [], []

def random_vertex(l):
    return np.random.random(2)*2*l-l

def find_segments(vertices, segments, d, epsilon,l,N):
    active_segments = [] #segmenty które będą się rozrastać
    segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
    tree = ckdtree.cKDTree(segments)
    for i in range(len(vertices)-1,-1,-1):
        dist, nearest_segment = tree.query(vertices[i])
        if dist < d:
            if not any(i in lista for lista in segments_vertices):
                vertices.pop(i)
                if N != 0:
                    new_vertex = random_vertex(l)
                    vertices.append(new_vertex)
                    N -= 1

    for i in range(len(vertices)):
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices, N

def find_segments_additive(vertices, modified_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices):
    tree = ckdtree.cKDTree(segments)
    for i in range(len(modified_vertices)-1,-1,-1): #bierzemy teraz modyfikowane wierzchołki
        dist, nearest_segment = tree.query(vertices[modified_vertices[i]])
        if dist < d:
            deleted = modified_vertices[i]
            if not any(deleted in lista for lista in segments_vertices): #sprawdzamy czy wszystkie segmenty dotarły do danego wierzchołka
                if N != 0:
                    new_vertex = random_vertex(l)
                    vertices[deleted] = new_vertex
                    N -= 1
                else:
                    modified_vertices.pop(i)
                    vertices.pop(deleted)
                    decrement(modified_vertices, deleted)
                    for lista in segments_vertices:
                        decrement(lista, deleted)
            else:
                delete(deleted, active_segments, segments_vertices, nearest_segment)


    for i in modified_vertices:
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices, N

def convert_list_to_typed(L):
    typed_L = numba.typed.List()
    for item in L:
        typed_L.append(item)
    return typed_L

# @numba.njit
def decrement(vertices, deleted):
    for i in range(len(vertices)):
        if vertices[i] > deleted:
            vertices[i] -= 1
        elif vertices[i] == deleted:
            raise ValueError("Multiple instances of vertex in the list")

def delete(deleted, active_segments, segments_vertices, nearest_segment):
    for i in range(len(active_segments)):
        if nearest_segment == active_segments[i]:
            segments_vertices[i].remove(deleted)
            if len(segments_vertices[i]) == 0:
                segments_vertices.pop(i)
                active_segments.pop(i)


def find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, ):
    dist, nearest_segment = tree.query(vertices[i])
    nearest_segments = tree.query_ball_point(vertices[i],dist*3) ## TODO: N_jobs
    # nearest_segments = np.arange(len(segments))
    nearest_segments = convert_list_to_typed(nearest_segments)
    segments_check(vertices[i], nearest_segments, np.array(segments))
    for s in nearest_segments:
        if segments[s] in active_segments:
            index = active_segments.index(segments[s])
            if not (i in segments_vertices[index]):
                segments_vertices[index].extend([i])
        else:
            active_segments.append(segments[s])
            segments_vertices.append([i])

def segments_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d,epsilon, l, N):
    recalibrate = False
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            recalibrate, modified_vertices = segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate)
            if recalibrate:
                active_segments, segments_vertices, N = find_segments_additive(active_vertices, modified_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices)
                recalibrate = False
                break

    return active_segments, segments_vertices, N

def segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate):
    r, r_list, dist_x, dist_y = compute_dist(i, active_vertices, active_segments, segments_vertices, d, )
    if r > d:
        new_seg = (active_segments[i][0]+dist_x,active_segments[i][1]+dist_y)
        for j in range(len(r_list)):
            x = active_vertices[segments_vertices[i][j]][0] - new_seg[0]
            y = active_vertices[segments_vertices[i][j]][1] - new_seg[1]
            if (x**2+y**2) > r_list[j]**2:
                recalibrate = True
                # recalibrate, modified_vertices = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
                break
        else:
            segments.append(new_seg)
            active_segments[i] = new_seg
            return recalibrate, None
    else:
        recalibrate = True

    recalibrate, modified_vertices = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
    return recalibrate, modified_vertices

def compute_dist(i, active_vertices, active_segments, segments_vertices, d, ):
    dist_x = 0
    dist_y = 0
    r_list = []
    for j in range(len(segments_vertices[i])):
        x = active_vertices[segments_vertices[i][j]][0] - active_segments[i][0]
        y = active_vertices[segments_vertices[i][j]][1] - active_segments[i][1]
        r = (x**2 + y**2)**0.5
        dist_x += x
        dist_y += y
        r_list.append(r)
    r = (dist_x**2 + dist_y**2)**0.5
    dist_x = dist_x*d/r
    dist_y = dist_y*d/r
    return r, r_list, dist_x, dist_y

def recalibration(i, r_list, segments_vertices, active_segments, active_vertices, segments, d, ):
    # breakpoint()
    closest_id = np.argmin(r_list)
    vertex = segments_vertices[i].pop(closest_id)
    modified_vertices = [vertex]
    if len(segments_vertices[i]) == 0:
        segments_vertices.pop(i)
        active_segments.pop(i)
        recalibrate = not any(vertex in lista for lista in segments_vertices)
    else:
        x = active_vertices[vertex][0] - active_segments[i][0]
        y = active_vertices[vertex][1] - active_segments[i][1]
        r = r_list[closest_id]
        if r >= d:
            new_seg = (active_segments[i][0]+x*d/r,active_segments[i][1]+y*d/r)
        else:
            new_seg = (active_vertices[vertex][0], active_vertices[vertex][1])
        segments.append(new_seg)
        active_segments.append(new_seg)
        segments_vertices.append([vertex])
        recalibrate = True
    return recalibrate, modified_vertices
