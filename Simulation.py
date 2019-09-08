import tqdm.autonotebook
import numpy as np
from scipy.spatial import ckdtree

def run(N,M,Frames,l,d,epsilon):
    segments, active_vertices, animation_vertices, animation_segments, active_segments, segments_vertices = reset()
    # active_segments = [] #segmenty które będą się rozrastać
    # segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
    for n in tqdm.autonotebook.tqdm(range(N)):
        new_vertex = random_vertex(l)
        active_vertices.append(new_vertex)
        active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon, active_segments, segments_vertices, new_vertex)
        for f in range(Frames):
            L = len(segments)
            active_segments, segments_vertices = segments_adding(M,active_vertices,active_segments,segments_vertices,segments,d,epsilon)
            if L != len(segments):
                animation_vertices.append(np.array(active_vertices))
                animation_segments.append(np.array(segments))

    active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon,)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))

    segments = np.vstack(np.array(segments)).T
    return [animation_segments,animation_vertices]

def reset():
    return [(0,0)], [], [], [], [], []

def random_vertex(l):
    return np.random.random(2)*2*l-l

def find_segments_additive(vertices, segments, d, epsilon, active_segments, segments_vertices, changed_vertices):
    tree = ckdtree.cKDTree(segments)
    for i in range(len(changed_vertices)-1,-1,-1):
        dist, nearest_segment = tree.query(changed_vertices[i])
        if dist < d:
            for i1 in range(len(segments_vertices)):
                for i2 in range(len(segments_vertices[i])):
                    if segments_vertices[i1][i2][0] == changed_vertices[i][0] and segments_vertices[i1][i2][1] == changed_vertices[i][1]:
            # if not any(i in lista for lista in segments_vertices):
                        done = changed_vertices.pop(i)
                        for j in range(len(vertices)-1,-1,-1):
                            if vertices[j][0] == done[0] and vertices[j][1] == done[1]:
                                del vertices[j]

    for i in range(len(changed_vertices)):
        find_segment(i, tree, d, segments, changed_vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices

def find_segments(vertices, segments, d, epsilon):
    active_segments = []
    segments_vertices = []
    tree = ckdtree.cKDTree(segments)
    for i in range(len(vertices)-1,-1,-1):
        dist, nearest_segment = tree.query(vertices[i])
        if dist < d:
            if not any(i in lista for lista in segments_vertices):
                vertices.pop(i)

    for i in range(len(vertices)):
        find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, )
    return active_segments, segments_vertices

def find_segment(i, tree, d, segments, vertices, active_segments, segments_vertices, ):
    dist, nearest_segment = tree.query(vertices[i])
    nearest_segments = tree.query_ball_point(vertices[i],dist*2) ## TODO: N_jobs
    xS = vertices[i][0]
    yS = vertices[i][1]
    for i1 in range(len(nearest_segments)-1,-1,-1):
        accepted = True
        x = segments[nearest_segments[i1]][0]
        y = segments[nearest_segments[i1]][1]
        dist_s = ((x-xS)**2 + (y-yS)**2)
        for i2, seg in enumerate(segments):
            if i2 == i1:
                continue
            xU = seg[0]
            yU = seg[1]
            dist_u = ((x-xU)**2 + (y-yU)**2)
            dist_su = ((xS-xU)**2 + (yS-yU)**2)
            if dist_s > max(dist_u, dist_su):
                accepted = False
                break
        if not accepted:
            nearest_segments.pop(i1)
    for s in nearest_segments:
        if (segments[s] in active_segments):
            index = active_segments.index(segments[s])
            # if (not (vertices[i] in segments_vertices[index])):
            segments_vertices[index].extend([vertices[i]])
        else:
            active_segments.append(segments[s])
            segments_vertices.append([vertices[i]])


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

def segments_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d,epsilon):
    recalibrate = False
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            recalibrate, changed_vertices = segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate)
            if recalibrate:
                active_segments, segments_vertices = find_segments_additive(active_vertices, segments, d, epsilon, active_segments, segments_vertices, changed_vertices)
                recalibrate = False
                break

    return active_segments, segments_vertices

def segment_adding(i, active_vertices, active_segments, segments_vertices, segments, d, recalibrate):
    changed_vertices = []
    r, r_list, dist_x, dist_y = compute_dist(i, active_vertices, active_segments, segments_vertices, d, )
    for j in range(len(r_list)):
        changed_vertices.append(segments_vertices[i][j])
    if r > d:
        new_seg = (active_segments[i][0]+dist_x,active_segments[i][1]+dist_y)
        for j in range(len(r_list)):
            x = segments_vertices[i][j][0] - new_seg[0]
            y = segments_vertices[i][j][1] - new_seg[1]
            if (x**2+y**2) > r_list[j]**2:
                recalibrate = True
                break
        if not recalibrate:
            segments.append(new_seg)
            active_segments[i] = new_seg
            return recalibrate, changed_vertices
    else:
        recalibrate = True


    recalibrate = recalibration(i ,r_list, segments_vertices, active_segments, active_vertices, segments, d, )
    return recalibrate, changed_vertices

def compute_dist(i, active_vertices, active_segments, segments_vertices, d, ):
    dist_x = 0
    dist_y = 0
    r_list = []
    for j in range(len(segments_vertices[i])):
        x = segments_vertices[i][j][0] - active_segments[i][0]
        y = segments_vertices[i][j][1] - active_segments[i][1]
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
        recalibrate = True
        for i in range(len(segments_vertices)):
            for j in range(len(segments_vertices[i])):
                if segments_vertices[i][j][0] == vertex[0] and segments_vertices[i][j][1] == vertex[1]:
                    recalibrate = False
    else:
        x = vertex[0] - active_segments[i][0]
        y = vertex[1] - active_segments[i][1]
        r = r_list[closest_id]
        new_seg = (active_segments[i][0]+x*d/r,active_segments[i][1]+y*d/r)
        segments.append(new_seg)
        segments_vertices.pop(i)
        active_segments.pop(i)
        recalibrate = True
    return recalibrate
