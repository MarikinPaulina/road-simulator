from Simulation import reset, find_segments, segments_adding
import numpy as np
import pytest

def test_lackOfLoopsCentered():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([0,1]))
    segments.append((2e-3,0))
    segments.append((-2e-3,0))
    segments.append((2*2e-3,0))
    segments.append((-2*2e-3,0))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(50):
        L = len(segments)
        active_segments, segments_vertices = segments_adding(10,active_vertices,active_segments,segments_vertices,segments,2e-3,2e-7)
        if L != len(segments):
            animation_vertices.append(np.array(active_vertices))
            animation_segments.append(np.array(segments))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))
    assert len(active_vertices) == 0
    assert len(segments) == 504

def test_lackOfLoopsSided():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([0,1]))
    segments.append((2e-3,0))
    segments.append((2*2e-3,0))
    segments.append((3*2e-3,0))
    segments.append((4*2e-3,0))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    for f in range(50):
        L = len(segments)
        active_segments, segments_vertices = segments_adding(10,active_vertices,active_segments,segments_vertices,segments,2e-3,2e-7)
        if L != len(segments):
            animation_vertices.append(np.array(active_vertices))
            animation_segments.append(np.array(segments))
    active_segments, segments_vertices = find_segments(active_vertices, segments,2e-3,2e-7)
    animation_vertices.append(np.array(active_vertices))
    animation_segments.append(np.array(segments))
    assert len(active_vertices) == 0
    assert len(segments) == 504

def test_twoEnds():
    segments, active_vertices, animation_vertices, animation_segments = reset()
    active_vertices.append(np.array([0.5,0]))
    segments.append((1,0))
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
    assert len(active_vertices) == 0
    assert len(segments) == 500
