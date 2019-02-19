# calcultates camera view from bounding boc

import math

# ewwork of
# scene size is [[x1,y1,z1],[x2,y2,z2]
def placed(scene_size, fudge=1, fov=30.0, rescale=400.0):
    # camera location & target
    cam_t = centroid(scene_size, rescale)
    # calculate fov distance
    distance = -fudge * (sphere(scene_size) / math.sin(fov / (2 * math.pi)))
    # rotate the point but angles
    cam_p = rot(distance / rescale, -25, 25)
    #cam_p = rot(distance / rescale, 20, 33)
    # offset by target move
    cam_p[0] = cam_p[0] + cam_t[0]
    cam_p[1] = cam_p[1] + cam_t[1]
    cam_p[2] = cam_p[2] + cam_t[2]
    # write
    data = {}
    xzy = lambda a: (a[0], a[2], a[1])  # x,z,y coordinates (not x,y,z)
    data["camera_target"] = ",".join("%g" % (val) for val in xzy(cam_t))
    data["camera_pos"] = ",".join("%g" % (val) for val in xzy(cam_p))
    # weird threejs cooreds
    # cam_p[1] = -cam_p[1]
    data["cam"] = xyz(cam_p)
    data["target"] = xyz(cam_t)
    data["distance"] = distance
    data["sphere"] = sphere(scene_size)
    data["scene"] = scene_size
    return data


def xyz(pos):
    return {"x": pos[0], "y": pos[1], "z": pos[2]}


def centroid(scene_size, rescale):
    x = (scene_size[1][0] + scene_size[0][0]) / 4.0
    y = (scene_size[1][1] + scene_size[0][1]) / 4.0
    z = (scene_size[1][2] + scene_size[0][2]) / 4.0
    return [x / rescale, y / rescale, z / rescale]


# calculate the bounding sphere
def sphere(scene_size):
    c = centroid(scene_size, 1)
    smin = scene_size[0]
    smax = scene_size[1]
    val = 2 * max(
        [
            hypot(c[0], smin[0]),
            hypot(c[1], smin[1]),
            hypot(c[2], smin[2]),
            hypot(c[0], smax[0]),
            hypot(c[1], smax[1]),
            hypot(c[2], smax[2]),
        ]
    )
    return val


def hypot(a, b):
    c = math.sqrt((a * a) + (b * b))
    return c


# rotate point around the  origin
def rot(d, alpha, beta):
    a = alpha / (2 * math.pi)
    b = beta / (2 * math.pi)
    x = d * math.cos(a) * math.cos(b)
    y = d * math.cos(a) * math.sin(b)
    z = d * math.sin(a)
    return [x, y, z]
