from flask import Blueprint, jsonify

bp = Blueprint("api", __name__, url_prefix="/api/v0/")
d = ""


@bp.route("/")
def index():
    return "Index"


@bp.route("/list/<path:modelname>")
def subcat(modelname):
    return jsonify(d.prefix(modelname))


@bp.route("/show/<path:modelname>")
def show(modelname):
    return jsonify(d.params(modelname))


@bp.route("/stat/unbuilt")
def unbuilt():
    un = []
    l = d.treeiter("export")
    for i in l:
        if (i.built == False) & (i.is_leaf == True):
            un.append(i.dir())
    return jsonify(un)


@bp.route("/stat/built")
def built():
    b = []
    l = d.treeiter("export")
    for i in l:
        if (i.built == True) & (i.is_leaf == True):
            b.append(i.info())
    return jsonify(b)


@bp.route("/stat/all")
def all():
    a = []
    l = d.treeiter("export")
    for i in l:
        if i.is_leaf == True:
            a.append(i.info())
        else:
            a.append(d.prefix(i.get_path()[1:]))
    return jsonify(a)


@bp.route("/stat/showcase")
def showcase():
    a = []
    l = d.treeiter("export/showcase")
    for i in l:
        if i.is_leaf == True:
            a.append(i.info())
    return jsonify(a)
