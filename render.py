from flask import Blueprint, Response, abort, send_file, request
import os

renderbp = Blueprint("render", __name__)


import json, time

event = []
# the directory
d = None


@renderbp.route("/render")
def render():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            if len(event) > 0:
                yield event.pop(0)
            else:
                time.sleep(1)

    return Response(eventStream(), mimetype="text/event-stream")


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
