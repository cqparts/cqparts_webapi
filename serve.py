#!/usr/bin/env python
import sys, os

# working inside the lib

import json
import yaml

from flask import Flask, jsonify, abort, render_template, request, session, redirect

import api
import cache
import views
import render
import directory
import landing

app = Flask(__name__)
app.secret_key = "sort of but not actually that secret"
app.register_blueprint(api.bp)
app.register_blueprint(cache.cachebp)
app.register_blueprint(render.renderbp)
d = directory.Directory("examples", "export")
api.d = d
render.d = d
cache.d = d

front = yaml.load(open('inf.yaml').read())

# don't cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    #    app.logger.error(session)
    return response


@app.route("/")
def base():
    session["bork"] = True
    return landing.get_landing(app,d,local=False)
    #return render_template("landing.html", date_fulla=front)


@app.route("/list/<path:modelname>")
def subcat(modelname):
    return render_template("list.html", dirs=d.prefix(modelname))

@app.route("/show/<path:modelname>", methods=["GET", "POST"])
def show_model(modelname):
    if request.method == "POST":
        v = request.form.copy()
        d.build_part(v)
    app.logger.error("%s", modelname)
    ob = d.params(modelname)
    return render_template("view.html", item=d.params(modelname))


@app.route("/rebuild", methods=["POST"])
def rebuild():
    return jsonify(request.form.items())


@app.route("/examples/<path:modelname>")
def example_redirect(modelname):
    return redirect("/show/"+d.base+"/"+modelname,code=302)

@app.route("/examples/")
def example_list():
    li = []
    l = d.treeiter("export")
    for i in l:
        if i.is_leaf == True:
            li.append(i.info())
    return render_template("everything.html", list=li)

print(app.url_map)
if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=8089)
