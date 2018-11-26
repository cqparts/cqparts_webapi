from flask import Blueprint, jsonify, render_template

cfg  = Blueprint("config", __name__, url_prefix="/config/")

class entry:
    def __init__(self,form,name,value):
        self.form = form
        self.name = name
        self.value = value

conf = []

def add(form,name,value):
    conf.append(entry(form,name,value))

add('bool','bob',True)
add('int','size',10)

@cfg.route("/")
def index():
    return render_template("config.html",conf=conf,data={})
