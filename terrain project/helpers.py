import math
import numpy as np

def normalize(v):
    return v / np.linalg.norm(v)


def look_at(eye, target):
    forward = normalize(target - eye)
    right = normalize(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)

    return np.array([
        [right[0],   right[1],   right[2],   -np.dot(right, eye)],
        [up[0],      up[1],      up[2],      -np.dot(up, eye)],
        [-forward[0],-forward[1],-forward[2], np.dot(forward, eye)],
        [0, 0, 0, 1]
    ], dtype="f4")


def perspective(fov, aspect, near, far):
    f = 1 / math.tan(math.radians(fov) / 2)

    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far),
               (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype="f4")

    #this whole thing is just a bunch of math thats unfortunately unavoidable so we're gonna keep it here