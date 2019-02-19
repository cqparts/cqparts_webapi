from flask import Blueprint, Response, abort, send_file, request
from flask import jsonify
import os

renderbp = Blueprint("render", __name__)


import json, time

event = []
# the directory
d = None

# send a single render
@renderbp.route("/render")
def render():
    l = d.treeiter("export")
    for i in l:
        data = i.info()
        if i.is_leaf == True:
            if i.built == True:
                if i.rendered == False:
                    if i.pending == False:
                        i.pending = True
                        return jsonify(data)
    return jsonify({"queue":"empty"}) 



@renderbp.route("/rendersizes")
def render_sizes():
    s = d.store.get_sizes()
    return jsonify(s)
    
# get posted image
@renderbp.route("/image", methods=["POST"])
def image():
    data = None
    try:
        data = request.files["objs"]
    except:
        abort(403)
        return
    export_path = d.export_prefix + os.sep + "img" + os.sep
    try:
        os.makedir(export_path)
    except:    
        pass
    data.save(export_path + data.filename)
    d.set_image(data.filename)
    return "OK"


# get zipped gltf
@renderbp.route("/zipped/<modelname>")
def zipped(modelname):
    v = d.get_name(modelname)
    if v is None:
        abort(404)
        return
    file_name = d.get_zipped(v)
    return send_file(
        file_name,
        mimetype="application/zip",
        as_attachment=True,
        attachment_filename=v.name + ".zip",
    )
