from flask import Blueprint, Response, abort, send_file, request
import os

cachebp = Blueprint("cache", __name__, url_prefix="/cache")

d = ""


@cachebp.route("/model/<modelname>/<filename>")
def model(modelname, filename):
    v = d.get_name(modelname)
    if v is None:
        abort(404)
        return
    path = "./" + v.gltf_path + "/" + filename
    return send_file(path)


@cachebp.route("/img/<path:modelname>")
def image(modelname):
    return
