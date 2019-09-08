import numpy as np
from Simulation import reset, find_segments, segments_adding
def test_straight():
    segments, active_vertices, animation_vertices, animation_segments, active_segments, segments_vertices = reset()
    active_vertices.append(np.array([0,1]))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(100):
        L = len(segments)
        active_segments, segments_vertices = segments_adding(10,active_vertices,active_segments,segments_vertices,segments,2e-3,2e-7)
        if L != len(segments):
            animation_vertices.append(np.array(active_vertices))
            animation_segments.append(np.array(segments))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))
    segments = np.vstack(np.array(segments)).T
    assert len(active_vertices) == 0
    assert len(animation_segments) == 51

def test_diagonal():
    segments, active_vertices, animation_vertices, animation_segments, active_segments, segments_vertices = reset()
    active_vertices.append(np.array([1,1]))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(100):
        L = len(segments)
        active_segments, segments_vertices = segments_adding(10,active_vertices,active_segments,segments_vertices,segments,2e-3,2e-7)
        if L != len(segments):
            animation_vertices.append(np.array(active_vertices))
            animation_segments.append(np.array(segments))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))
    segments = np.vstack(np.array(segments)).T
    assert len(active_vertices) == 0
    assert len(animation_segments) == 72
