import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree
from segcheck import segments_check
import numba.typed

def run(N,M,Frames,l,d,epsilon, number_of_vertices = 1, test=False, initial_vertices = None, initial_segments=None):
    segments, active_vertices, animation_vertices, animation_segments = reset()
    # new_verteces = []
    if not (initial_segments is None):
        segments = initial_segments
    if initial_vertices is None:
        for i in range(number_of_vertices):
            new_vertex = random_vertex(l)
            # new_verteces.append(new_vertex)
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
                    if N%100 == 0:
                        print(N)

    for i in range(len(vertices)):
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices, N

def convert_list_to_typed(L):
    typed_L = numba.typed.List()
    for item in L:
        typed_L.append(item)
    return typed_L

def find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, ):
    dist, nearest_segment = tree.query(vertices[i])
    nearest_segments = tree.query_ball_point(vertices[i],dist*2) ## TODO: N_jobs
    nearest_segments = convert_list_to_typed(nearest_segments)
    segments_check(vertices[i], nearest_segments, np.array(segments))
    for s in nearest_segments:
        if segments[s] in active_segments:
            index = active_segments.index(segments[s])
            segments_vertices[index].extend([i])
        else:
            active_segments.append(segments[s])
            segments_vertices.append([i])


    # close = ((dist-dist[0])< 10*d)
    # nearest_segments = nearest_segments[close]
    # close = np.ones(len(nearest_segments), dtype=bool)
    # for s in range(1,len(nearest_segments)):
    #     seg_dist = np.linalg.norm(np.array(segments[nearest_segments[0]])-np.array(segments[nearest_segments[s]]))
    #     if seg_dist < 5*d:
    #         close[s] = False
    # for s in nearest_segments[close]:
    #     if segments[s] in active_segments:
    #         index = active_segments.index(segments[s])
    #         segments_vertices[index].extend([i])
    #     else:
    #         active_segments.append(segments[s])
    #         segments_vertices.append([i])

def segments_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d,epsilon, l, N):
    recalibrate = False
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            recalibrate = segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate)
            if recalibrate:
                active_segments, segments_vertices, N = find_segments(active_vertices, segments,d,epsilon, l, N)
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
                break
        if not recalibrate:
            segments.append(new_seg)
            active_segments[i] = new_seg
            return recalibrate
    else:
        recalibrate = True


    recalibrate = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
    return recalibrate

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
    closest_id = np.argmin(r_list)
    vertex = segments_vertices[i].pop(closest_id)
    if len(segments_vertices[i]) == 0:
        segments_vertices.pop(i)
        active_segments.pop(i)
        recalibrate = not any(vertex in lista for lista in segments_vertices)
    else:
        x = active_vertices[vertex][0] - active_segments[i][0]
        y = active_vertices[vertex][1] - active_segments[i][1]
        r = r_list[closest_id]
        new_seg = (active_segments[i][0]+x*d/r,active_segments[i][1]+y*d/r)
        segments.append(new_seg)
        recalibrate = True
    return recalibrate
