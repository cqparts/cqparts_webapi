from flask import Blueprint

cachebp = Blueprint("cache", __name__, url_prefix="/cache")


@cachebp.route("/<path:modelname>")
def cache(modelname):
    return modelname
