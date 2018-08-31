from flask import Blueprint, jsonify

bp = Blueprint('api', __name__, url_prefix='/api/v0/')
d = ''

@bp.route('/')
def index():
    return 'Index'

@bp.route('/list/<path:modelname>')
def subcat(modelname):
    return jsonify(d.prefix(modelname))

@bp.route('/show/<path:modelname>')
def show(modelname):
    return jsonify(d.params(modelname))


