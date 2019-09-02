from tqdm.autonotebook import tqdm
import numpy as np
from scipy.spatial import ckdtree

def run(N,M,Frames,l,d,epsilon):
    segments, active_vertices, animation_vertices, animation_segments = reset()
    for n in tqdm(range(N)):
        active_vertices.append(random_vertex(l))
        active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon)
        for f in range(Frames):
            L = len(segments)
            active_segments, segments_vertices = segments_adding(M,active_vertices,active_segments,segments_vertices,segments,d,epsilon)
            if L != len(segments):
                animation_vertices.append(np.array(active_vertices))
                animation_segments.append(np.array(segments))

    active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))

    segments = np.vstack(np.array(segments)).T
    return [animation_segments,animation_vertices]

def reset():
    return [(0,0)], [], [], []

def random_vertex(l):
    return np.random.random(2)*2*l-l

def find_segments(vertices, segments, d, epsilon):
    active_segments = [] #segmenty które będą się rozrastać
    segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
    tree = ckdtree.cKDTree(segments)
    for i in range(len(vertices)-1,-1,-1):
        dist, nearest_segments = tree.query(vertices[i])
        if dist < d:
            vertices.pop(i)
    for i in range(len(vertices)):
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices

def find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, ):
    dist, nearest_segments = tree.query(vertices[i],5)
    close = ((dist-dist[0])< d) #0.001
    nearest_segments = nearest_segments[close]
    close = np.ones(len(nearest_segments), dtype=bool)
    for s in range(1,len(nearest_segments)):
        seg_dist = np.linalg.norm(np.array(segments[nearest_segments[0]])-np.array(segments[nearest_segments[s]]))
        if seg_dist < 5*d:
            close[s] = False
    for s in nearest_segments[close]:
        if segments[s] in active_segments:
            index = active_segments.index(segments[s])
            segments_vertices[index].extend([i])
        else:
            active_segments.append(segments[s])
            segments_vertices.append([i])

def segments_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d,epsilon):
    recalibrate = False
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            recalibrate = segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate)
            if recalibrate:
                active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon)
                recalibrate = False
                break

    return active_segments, segments_vertices

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
    recalibrate = True

    recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
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
    else:
        x = active_vertices[vertex][0] - active_segments[i][0]
        y = active_vertices[vertex][1] - active_segments[i][1]
        r = r_list[closest_id]
        new_seg = (active_segments[i][0]+x*d/r,active_segments[i][1]+y*d/r)
        segments.append(new_seg)
