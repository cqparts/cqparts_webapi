from flask import Blueprint, Response, abort, send_file, request
import os
from flask import current_app

cachebp = Blueprint("cache", __name__, url_prefix="/cache")

d = ""


@cachebp.route("/model/<modelname>/<filename>")
def model(modelname, filename):
    v = d.get_name(modelname)
    current_app.logger.error(modelname)
    current_app.logger.error(filename)
    current_app.logger.error(v.gltf_path)
    if v is None:
        abort(404)
        return
    path = v.gltf_path[1:] + "/" + filename
    return send_file(path)


@cachebp.route("/img/<modelname>")
def image(modelname):
    name = modelname.split(".")[0]
    v = d.get_name(name)
    if v is None:
        abort(404)
        return
    path = "./" + d.export_prefix + "/img/" + modelname
    return send_file(path)
