def random_vertex(l):
    import numpy as np

    x, y = np.random.random(2)*2*l-l
    return np.array([x,y])

def find_segments(vertices, segments, d, epsilon):
    from scipy.spatial import ckdtree

    active_segments = [] #segmenty które będą się rozrastać
    segments_vertices = [] #krawędzie do których będzie rozrastać się segment na odpowiednim miejscu powyżej
    tree = ckdtree.cKDTree(segments)
    for i in range(len(vertices)-1,-1,-1):
        dist, nearest_segments = tree.query(vertices[i])
        if dist < d:
            del vertices[i]
    for i in range(len(vertices)):
        dist, nearest_segments = tree.query(vertices[i],5)
        close = ((dist-dist[0])<epsilon)
        for s in nearest_segments[close]:
            if segments[s] in active_segments:
                index = active_segments.index(segments[s])
                segments_vertices[index].extend([i])
            else:
                active_segments.append(segments[s])
                segments_vertices.append([i])

    return active_segments, segments_vertices


def segment_adding(M:int, active_vertices, active_segments, segments_vertices, segments,d):
    for m in range(M):
        for i in range(len(active_segments)-1, -1, -1):
            dist_x = 0
            dist_y = 0
            r_list = []
            for j in range(len(segments_vertices[i])):
                x = active_vertices[segments_vertices[i][j]][0] - active_segments[i][0]
                y = active_vertices[segments_vertices[i][j]][1] - active_segments[i][1]
                dist_x += x
                dist_y += y
                r_list.append((x**2 + y**2)**0.5)
            r = (dist_x**2 + dist_y**2)**0.5
            if r > d:
                new_seg = (active_segments[i][0]+dist_x*d/r,active_segments[i][1]+dist_y*d/r)
#                 print(((dist_x/r*d)**2+(dist_y/r*d)**2)**0.5)
                segments.append(new_seg)
#                 visual.append([active_segments[i],new_seg])
                active_segments[i] = new_seg
            else:
                closest_id = r_list.index(min(r_list))
                vertex = segments_vertices[i][closest_id]
                del segments_vertices[i][closest_id]
                if len(segments_vertices[i]) == 0:
                    del segments_vertices[i]
                    del active_segments[i]
                else:
                    x = active_vertices[vertex][0] - active_segments[i][0]
                    y = active_vertices[vertex][1] - active_segments[i][1]
                    r = r_list[closest_id]
                    new_seg = (active_segments[i][0]+x*d/r,active_segments[i][1]+y*d/r)
                    segments.append(new_seg)
#                     visual.append([active_segments[i],new_seg])
                    active_segments.append(new_seg)
                    segments_vertices.append([vertex])

#                         segments_vertices.remove(segments_vertices[i])
#                         active_segments.remove(active_segments[i])

def run(N,M,Frames,l,d,epsilon):
    from tqdm.autonotebook import tqdm
    import numpy as np
    from scipy.spatial import ckdtree

    segments = [(0,0)]
    active_vertices = []
    animation_vertices = []
    animation_segments = []
    for n in tqdm(range(N)):
        active_vertices.append(random_vertex(l))
        active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon)
        for f in range(Frames):
            segment_adding(M,active_vertices,active_segments,segments_vertices,segments,d)
            if len(active_segments) != 0:
                animation_vertices.append(np.array(active_vertices))
                animation_segments.append(np.array(segments))

    active_segments, segments_vertices = find_segments(active_vertices, segments,d,epsilon)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))

    # active_vertices = np.vstack(active_vertices).T
    segments = np.vstack(np.array(segments)).T
    return [animation_segments,animation_vertices]
