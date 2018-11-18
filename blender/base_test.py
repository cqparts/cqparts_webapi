
# run me from blender 
import json
import requests
import time
import os
import zipfile ,io 
import bpy

target =  os.environ['CQPARTS_SERVER']
folder = "/opt/stash/"
section = ""
render_sets = {}


def tryAgain(retries=0):
    if retries > 50: return
    is_data = False
    try:
        r = requests.get(target+'/render', stream=True)
        print("connected to "+target)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                spl = decoded_line.split(":",1)
                print(spl)
                if is_data:
                    if spl[0] == 'data':
                        if section == 'render':
                            data = spl[1]
                            jdata = json.loads(data)
                            is_data == False
                            render_this(jdata)
                if spl[0] == "event":
                    if spl[1] != '':
                        section = spl[1]
                        is_data = True

    except Exception as e:
        print(e)
        time.sleep(1.5*retries)
        retries+=1
        print ("retries :"+str(retries))
        tryAgain(retries)

def render_this(jdata):
    name = jdata['name']
    print(jdata)
    r = requests.get(target+'/zipped/'+name,stream=True)
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(folder)
    except:
        print("BROKEN ZIP :"+folder)
    print(r)
    make_blender(name,jdata['cam'],jdata['target'])
    uploader(name)

# https://github.com/ksons/gltf-blender-importer
def make_blender(name,cam_loc,tgt_loc):
    # TODO should pass render sets from the cqpart-server
    # split me into a dictionary
    multiplier =  100
    res = (320,240)
    samples = 60 
    #res = (1024,768)
    #samples = 200
    size_per = 100

    bpy.ops.wm.read_homefile()
    bpy.ops.wm.addon_enable(module="io_scene_gltf")
    # maybe script build the entire scene
    bpy.ops.scene.new(type='NEW')
    #bpy.context.scene.name = 'cqparts'
    # make the world
    bpy.ops.world.new()
    world = bpy.data.worlds['World.001']
    world.name = 'NewWorld'
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (1,1,1,1)
    bg.inputs[1].default_value = (0.5)
    world.light_settings.use_ambient_occlusion = True

    bpy.context.scene.world = world

    #theScene = bpy.data.scenes['cqparts']
    theScene = bpy.context.scene
    theScene.cycles.samples = samples
    theScene.cycles.film_transparent = True 
    theScene.render.filepath = folder+name+".png"
    theScene.render.resolution_x = res[0]
    theScene.render.resolution_y = res[1]
    theScene.render.resolution_percentage = size_per
    # make and bind the camera
    bpy.ops.object.camera_add()
    cam = bpy.context.selected_objects[0]
    bpy.context.scene.camera = cam
    cam.location = (-cam_loc['x']*multiplier,cam_loc['z']*multiplier,cam_loc['y']*multiplier)
    # add the track
    bpy.ops.object.constraint_add(type="TRACK_TO")

    # make the target and track the camera
    bpy.ops.object.empty_add(type='SPHERE')
    tgt  = bpy.context.selected_objects[0]
    tgt.name = "cam_target"
    tgt.location = (-tgt_loc['x']*multiplier,tgt_loc['z']*multiplier,tgt_loc['y']*multiplier)
    # select the camers
    track = cam.constraints["Track To"]
    track.target = bpy.data.objects['cam_target']
    track.up_axis = 'UP_Y'
    track.track_axis = 'TRACK_NEGATIVE_Z'

    # hemisphere
    bpy.ops.object.lamp_add(type='AREA')
    lamp = bpy.context.selected_objects[0]
    lamp.location = (0,1,20)
    # lamp 1
    bpy.ops.object.lamp_add(type='POINT')
    lamp = bpy.context.selected_objects[0]
    lamp.location = (50,50,50)

    # lamp 2
    bpy.ops.object.lamp_add(type='POINT')
    lamp2 = bpy.context.selected_objects[0]
    lamp2.location = (0,0,-50)

    bpy.ops.import_scene.gltf(filepath=folder+name+"/out.gltf")
    # this does not work second time.
    try:
        outer = theScene.objects['out']
        outer.scale = (100,100,100)
        bpy.ops.render.render(write_still=True)
        bpy.ops.wm.save_as_mainfile(filepath=folder+name+'.blend')
        outer.select
        bpy.ops.object.delete()
        bpy.ops.scene.delete()
    except:
        print("FAIL")
        for i in theScene.objects:
            print(i)

def uploader(name):
    file_ref = ('objs',(name+".png",open(folder+name+".png","rb")))
    requests.post(target+'/image',files=[file_ref])

print ("Running Blender Render runner")
tryAgain()
