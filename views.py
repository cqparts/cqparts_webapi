# calcultates camera view from bounding boc

import math
# ewwork of 
# scene size is [[x1,y1,z1],[x2,y2,z2]
def placed(scene_size,fudge=2.4,fov=30.0,rescale=1000.0):
    # camera location & target
    cnt = centroid(scene_size,rescale) 
    cam_t = cnt #[0,0,cnt[2]]
    # calculate fov distance 
    distance = -fudge*(sphere(scene_size)/ math.sin(fov/(2*math.pi)))
    # rotate the point but angles
    cam_p = rot(distance/rescale,45,45)
    # offset by target move
    #cam_p[0] = cam_p[0] - cam_t[0]
    #cam_p[1] = cam_p[1] - cam_t[1]
    #cam_p[2] = cam_p[2] - cam_t[2]
    # write
    data = {}
    xzy = lambda a: (a[0], a[2], -a[1])  # x,z,y coordinates (not x,y,z)
    data['camera_target']=','.join("%g" % (val) for val in xzy(cam_t)) 
    data['camera_pos']=','.join("%g" % (val) for val in xzy(cam_p))
    data['distance'] = distance
    data['sphere'] = sphere(scene_size)
    return data


def centroid(scene_size,rescale):
    x = (scene_size[1][0] + scene_size[0][0])/2.0
    y = (scene_size[1][1] + scene_size[0][2])/2.0
    z = (scene_size[1][2] + scene_size[0][2])/2.0
    return [x/rescale,y/rescale,z/rescale]

# calculate the bounding sphere
def sphere(scene_size):
    c = centroid(scene_size,1)
    mx =  scene_size[0]
    a = math.sqrt((c[0]*c[0])+(mx[0]*mx[0]))
    b = math.sqrt((c[1]*c[1])+(mx[1]*mx[1]))
    c = math.sqrt((c[2]*c[2])+(mx[2]*mx[2]))
    val = max([a,b,c])*2
    return val
     
# rotate point around the  origin 
def rot(d,alpha,beta):
    a = alpha/(2*math.pi)
    b = beta/(2*math.pi)
    x = d*math.cos(a)*math.cos(b)
    y = d*math.cos(a)*math.sin(b)
    z = d*math.sin(a)
    return [x,y,z]
