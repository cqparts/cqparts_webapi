# calcultates camera view from bounding boc

import math

# reference https://cubehero.com/2013/05/15/how-to-automatically-choose-a-camera-viewing-angle-of-any-3d-model/

# rework of
# scene size is [[x1,y1,z1],[x2,y2,z2]
def placed(scene_size,tweak=0.9 , fov=30.0, rescale=520.0):
    # camera location & target
    cam_t = centroid(scene_size,rescale)
    # rotate the point but angles
    l , w , h = lwh(scene_size)
    # polar coordinates
    phi = -(math.pi/3.0) * math.exp(-h/((l+w)))
    theta = (math.pi) + (math.pi/2.0) * math.exp(-w/l)
    #theta = 0 
    #phi = math.pi/2.0
    fovr = math.atan(math.radians(1.5*fov))*tweak
    radius = max([w/fovr,l/fovr,h/fovr])
 
    cam_p = rot(radius,phi,theta)
    # offset by target move
    cam_p[0] = (cam_p[0])/ rescale  + cam_t[0]
    cam_p[1] = (cam_p[1])/rescale  + cam_t[1]
    cam_p[2] = (cam_p[2])/rescale  + 3*cam_t[2]

    # write
    data = {}
    xzy = lambda a: (a[0], a[2], a[1])  # x,z,y coordinates (not x,y,z)
    data["camera_target"] = ",".join("%g" % (val) for val in xzy(cam_t))
    data["camera_pos"] = ",".join("%g" % (val) for val in xzy(cam_p))
    # weird threejs cooreds
    # cam_p[1] = -cam_p[1]
    data["cam"] = xyz(cam_p)
    data["target"] = xyz(cam_t)
    data["sphere"] = sphere(scene_size)
    data["scene"] = scene_size
    data["lwh"] = [l,w,h]
    data["ptr"] = [ phi,theta,radius ]
    return data


def xyz(pos):
    return {"x": pos[0], "y": pos[1], "z": pos[2]}


def lwh(scene_size):
    l = abs(scene_size[0][0] - scene_size[1][0]) 
    w = abs(scene_size[0][1] - scene_size[1][1])
    h = abs(scene_size[0][2] - scene_size[1][2])
    return [l,w,h]

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
def rot(radius,theta,phi):
    x = radius * math.sin(theta) * math.cos(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(theta)
    return [x, y, z]
