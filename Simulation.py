import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree
from segcheck import segments_check
import numba.typed, numba

def random_vertex(l, shapeAndDistribution):
    if shapeAndDistribution == 'homo square':
        return np.random.random(2)*2*l-l
    elif shapeAndDistribution == 'homo circle':
        r = np.random.random()
        phi = np.random.random()*2*np.pi
        return np.array([r*np.cos(phi),r*np.sin(phi)])
    elif shapeAndDistribution == 'normal':
        return np.random.normal(0,l,size=2)



def run(N,M,Frames,l,d,epsilon, number_of_vertices = 1, shapeAndDistribution=None, test=False, initial_vertices = None, initial_segments=None):
    segments, active_vertices, animation_vertices, animation_segments_index = reset()
    if not (initial_segments is None):
        segments = initial_segments
    if initial_vertices is None:
        for i in range(number_of_vertices):
            new_vertex = random_vertex(l,shapeAndDistribution)
            active_vertices.append(new_vertex)
    else:
        active_vertices = initial_vertices

    with tqdm.autonotebook.tqdm(total=N) as progressbar:
        N_new = N - len(active_vertices)
        active_segments, segments_vertices, N_new = find_segments(active_vertices, segments,d,epsilon,l, N_new,shapeAndDistribution)
        Ndelta, N = N - N_new, N_new
        progressbar.update(Ndelta)
        while len(active_vertices) != 0:
            for f in range(Frames):
                L = len(segments)
                active_segments, segments_vertices, N_new = segments_adding(M,active_vertices,active_segments,segments_vertices,segments,d,epsilon, l, N,shapeAndDistribution)
                Ndelta, N = N - N_new, N_new
                progressbar.update(Ndelta)
                if L != len(segments):
                    animation_vertices.append(np.array(active_vertices))
                    animation_segments_index.append(len(segments))

    active_segments, segments_vertices, N = find_segments(active_vertices, segments,d,epsilon, l, N, shapeAndDistribution)
    animation_vertices.append(np.array(active_vertices))
    animation_segments_index.append(len(segments)-1)
    animation_segments = np.array(segments)

    if test:
        return_pack = {
        "active_vertices" : active_vertices,
        "animation_segments" : animation_segments,
        "animation_vertices" : animation_vertices,
        "animation_segments_index" : animation_segments_index,
        "segments" : segments}
        return return_pack
    else:
        return [animation_segments, animation_segments_index, animation_vertices]

def reset():
    return [(0,0)], [], [], []

def find_segments(vertices, segments, d, epsilon,l,N,shapeAndDistribution):
    active_segments = [] #segmenty które będą się rozrastać
    segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
    tree = ckdtree.cKDTree(segments)
    for i in range(len(vertices)-1,-1,-1):
        dist, nearest_segment = tree.query(vertices[i])
        if dist < d:
            if not any(i in lista for lista in segments_vertices):
                vertices.pop(i)
                if N != 0:
                    new_vertex = random_vertex(l,shapeAndDistribution)
                    vertices.append(new_vertex)
                    N -= 1

    for i in range(len(vertices)):
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices, N

def find_segments_additive(tree, vertices, modified_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices,shapeAndDistribution):
    for i in range(len(modified_vertices)-1,-1,-1): #bierzemy teraz modyfikowane wierzchołki
        dist, nearest_segment = tree.query(vertices[modified_vertices[i]])
        if dist < d:
            deleted = modified_vertices[i]
            if not any(deleted in lista for lista in segments_vertices): #sprawdzamy czy wszystkie segmenty dotarły do danego wierzchołka
                if N != 0:
                    new_vertex = random_vertex(l,shapeAndDistribution)
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
    for i in range(len(active_segments)-1,-1,-1):
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
        if s in active_segments:
            index = active_segments.index(s)
            if not (i in segments_vertices[index]):
                segments_vertices[index].extend([i])
        else:
            active_segments.append(s)
            segments_vertices.append([i])

def segments_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d,epsilon, l, N,shapeAndDistribution):
    recalibrate = False
    # shuffleB = False
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            recalibrate, shuffleB, modified_vertices, i = segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate)
            if shuffleB or recalibrate:
                tree = ckdtree.cKDTree(segments)
                if recalibrate:
                    active_segments, segments_vertices, N = find_segments_additive(tree, active_vertices, modified_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices,shapeAndDistribution)
                    recalibrate = False
                    break
                if shuffleB:
                    active_segments, segments_vertices = shuffle(tree, i, active_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices)
                    shuffleB = False
                    break

    return active_segments, segments_vertices, N

def segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate):
    r, r_list, dist_x, dist_y = compute_dist(i, segments, active_vertices, active_segments, segments_vertices, d, )
    if r > d:
        new_seg = (segments[active_segments[i]][0]+dist_x, segments[active_segments[i]][1]+dist_y)
        for j in range(len(r_list)):
            x = active_vertices[segments_vertices[i][j]][0] - new_seg[0]
            y = active_vertices[segments_vertices[i][j]][1] - new_seg[1]
            if (x**2+y**2) > r_list[j]**2:
                recalibrate = True
                # recalibrate, modified_vertices = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
                break
        else:
            segments.append(new_seg)
            active_segments[i] = len(segments)-1
            return False, False, None, i
    else:
        recalibrate = True

    recalibrate, shuffleB, modified_vertices, i = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
    return recalibrate, shuffleB, modified_vertices, i

def shuffle(tree, i, active_vertices, segments, d, epsilon,l,N, active_segments, segments_vertices):
    # breakpoint()
    if i == -1 or len(segments) < 2:
        return active_segments, segments_vertices
    l = len(segments) if len(segments) < 5 else 5
    dist, potential_segs = tree.query(np.array(segments[active_segments[i]]), l)
    for v in range(len(segments_vertices[i])-1,-1,-1):
        v = segments_vertices[i][v]
        dist = []
        for s in potential_segs:
            dist.append((active_vertices[v][0] - segments[s][0])**2 + (active_vertices[v][1] - segments[s][1])**2)
        closest = potential_segs[np.argmin(dist)]
        if closest != active_segments[i]:
            if not (closest in active_segments):
                segments_vertices[i].remove(v)
                active_segments.append(closest)
                segments_vertices.append([v])
            elif not v in segments_vertices[active_segments.index(closest)]:
                segments_vertices[i].remove(v)
                index = active_segments.index(closest)
                if not (v in segments_vertices[index]):
                    segments_vertices[index].extend([v])


            # if closest in active_segments and not any(v in segments_vertices[active_segments.index(closest)]):
            #     index = active_segments.index(closest)
            #     if not (v in segments_vertices[index]):
            #         segments_vertices[index].extend([v])
            # else:
            #     active_segments.append(closest)
            #     segments_vertices.append([v])
    if len(segments_vertices[i]) == 0:
        active_segments.pop(i)
        segments_vertices.pop(i)


    return active_segments, segments_vertices


def compute_dist(i, segments, active_vertices, active_segments, segments_vertices, d, ):
    dist_x = 0
    dist_y = 0
    r_list = []
    for j in range(len(segments_vertices[i])):
        x = active_vertices[segments_vertices[i][j]][0] - segments[active_segments[i]][0]
        y = active_vertices[segments_vertices[i][j]][1] - segments[active_segments[i]][1]
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
    shuffleB = True
    if len(segments_vertices[i]) == 0:
        segments_vertices.pop(i)
        active_segments.pop(i)
        i = -1
    else:
        x = active_vertices[vertex][0] - segments[active_segments[i]][0]
        y = active_vertices[vertex][1] - segments[active_segments[i]][1]
        r = r_list[closest_id]
        if r >= d:
            new_seg = (segments[active_segments[i]][0]+x*d/r,segments[active_segments[i]][1]+y*d/r)
        else:
            new_seg = (active_vertices[vertex][0], active_vertices[vertex][1])
        segments.append(new_seg)
        active_segments.append(len(segments)-1)
        segments_vertices.append([vertex])
        shuffleB = True
    recalibrate = not any(vertex in lista for lista in segments_vertices)
    return recalibrate, shuffleB, modified_vertices, i
