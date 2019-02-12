#!/usr/bin/env python
import sys, os

# working inside the lib

import json
import yaml
import uuid

from flask import Flask, jsonify, abort, render_template, request, session, redirect

import api
import cache
import views
import render
import directory
import landing
import sess
import widgets
import plugins
import importer

app = Flask(__name__)

#app.debug = True
app.register_blueprint(api.bp)
app.register_blueprint(cache.cachebp)
app.register_blueprint(render.renderbp)

i = importer.importotron(importer.mods)
d = directory.Directory("examples", "export")
api.d = d
render.d = d
cache.d = d
widgets.d = d

app.secret_key = os.environ["CQPARTS_SECURE"]
app.session_interface = sess.SessionCollection(d.store)

# don't cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    #    app.logger.error(session)
    return response


@app.before_request
def build_sess():
    if not "id" in session:
        session["id"] = uuid.uuid4()
        session.permanent=True

@app.route("/landing")
def land():
    return landing.get_landing(app,d,local=False)

@app.route("/")
def base():
    return widgets.front(app)


@app.route("/list/<path:modelname>")
def subcat(modelname):
    return render_template("list.html", dirs=d.prefix(modelname),data={})

@app.route("/show/<path:modelname>", methods=["GET", "POST"])
def show_model(modelname):
    if request.method == "POST":
        v = request.form.copy()
        d.build_part(v)
    app.logger.error("%s", modelname)
    ob = d.params(modelname)
    plug = plugins.list()
    return render_template("view.html", item=d.params(modelname),plug=plug)


@app.route("/rebuild", methods=["POST"])
def rebuild():
    return jsonify(request.form.items())


@app.route("/examples/<path:modelname>")
def example_redirect(modelname):
    return redirect("/show/"+d.base+"/"+modelname,code=302)

@app.route("/config")
def actions():
    return render_template("config.html", data={})

@app.route("/examples/")
def example_list():
    li = []
    l = d.treeiter("export")
    for i in l:
        if i.is_leaf == True:
            li.append(i.info())
    return render_template("everything.html", list=li,data={})

print(app.url_map)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089)
