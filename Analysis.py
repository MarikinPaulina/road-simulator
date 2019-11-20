from tqdm.autonotebook import tqdm
import numpy as np

def make_polygons(segments, vertices, d):
    vertices = np.unique(np.array(flat_list(vertices)), axis = 0)
    segments_neighbor_count = SNC(segments, d)




def SNC(segments, d):
    '''segments neighbor count'''
    d *= 1.01 # tolerance

    snc = np.zeros(segments.shape[0])
    for i in range(len(snc)):
        dist2 = (segments[:, 0] - segments[i, 0]) ** 2 + (segments[:, 1] - segments[i, 1]) ** 2
        snc[i] = (dist2 < d ** 2).sum() - 1
    return snc

def flat_list(list):
    out = []
    for sublist in list:
        for item in sublist:
            out.append(item)
    return out