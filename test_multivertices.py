from Simulation import reset, find_segments, segments_adding
import numpy as np
import pytest

def test_twoToPlay():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([1,1]))
    active_vertices.append(np.array([1,-1]))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(200):
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
    assert len(animation_segments) == 101 #Docierają w różnych (o jeden) czasach przez wypustki. I tak samo wszędzie poniżej

def test_cross():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([1,1]))
    active_vertices.append(np.array([1,-1]))
    active_vertices.append(np.array([1.74,0]))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(200):
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
    assert len(animation_segments) == 102

# @pytest.mark.xfail
def test_simultaneous_growing():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([1,1]))
    active_vertices.append(np.array([1,-1]))
    active_vertices.append(np.array([0.5,0.5]))
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
    assert len(animation_segments) == 91

def test_simultaneous_breach():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([1,1]))
    active_vertices.append(np.array([1,-1]))
    active_vertices.append(np.array([0.5,0.5]))
    active_vertices.append(np.array([0.5,-0.5]))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(150):
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
    assert len(animation_segments) < 91
