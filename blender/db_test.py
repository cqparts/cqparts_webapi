
from sqlalchemy import *
from sqlalchemy.sql import and_, or_, not_

# from directory import thing
import json
import os
import requests
import time
import os
import zipfile ,io 
import bpy

# environmental variable so it does not get published
# should be in the form
# postgresql+psycopg2://user:password@host/database
sql_string = os.environ["CQPARTS_DB"]
target =  os.environ['CQPARTS_SERVER']
target =  "http://localhost:8089" #os.environ['CQPARTS_SERVER']

folder = "/opt/stash/"
section = ""
render_sets = {}

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
    #res = (320,240)
    #samples = 90 
    res = (640,480)
    samples = 500 
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
    try:
        requests.post(target+'/image',files=[file_ref])
    except:
        print("upload fail")
        
class Incoming:
    def __init__(self, prefix="cache"):
        self.db = create_engine(sql_string)
        self.metadata = MetaData(self.db)
        self.metadata.reflect(self.db)
        self.things = self.metadata.tables["things"]
        self.conn = self.db.connect()


    def mark(self,name):
        print(name)
        upd = self.things.update().where(
                self.things.c.name == name,
        )
        self.conn.execute(upd, render=True)

    def list(self):
        print("Fetching New")
        s = select([self.things]).where(self.things.c.render == False)
        result = self.conn.execute(s)
        l = []
        for row in result:
            l.append(row)
        for row in l:
            data = {}
            data['name'] = row.name
            js = json.loads(row.jsondata)
            print(js)
            data['cam']  = js['view']['cam']
            data['target']  = js['view']['target']
            render_this(data)
            self.mark(data['name'])

i = Incoming()
while True:
    i.list()
    time.sleep(10)

