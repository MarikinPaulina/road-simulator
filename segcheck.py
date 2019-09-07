import numpy as np

def segments_check(vertex, nearest_segments, segments, ):
    """

    """
    xS = vertex[0]
    yS = vertex[1]
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
