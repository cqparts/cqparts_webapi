#!/usr/bin/env python
import sys, os

# working inside the lib

import json
import yaml
import uuid

from flask import Flask, jsonify, abort, render_template, request, session

import api
import cache
import views
import render
import directory
import landing
import sessions

app = Flask(__name__)

app.secret_key = os.environ["CQPARTS_SECURE"]
#app.debug = True
app.register_blueprint(api.bp)
app.register_blueprint(cache.cachebp)
app.register_blueprint(render.renderbp)
d = directory.Directory("examples", "export")
api.d = d
render.d = d
cache.d = d

sess = sessions.SessionCollection(d.store)

# don't cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    #    app.logger.error(session)
    return response


@app.before_request
def build_sess():
    if session.has_key("id"):
        s = sess.get(session['id'])
        app.logger.error("have %s", s)
#    else:
#        "create key"
#        s = sess.new()
#        session["id"] = s.uuid 
#        app.logger.error("create key %s", s)

@app.route("/")
def base():
    return landing.get_landing(app,d,local=False)
    #return render_template("landing.html", data=front)


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


print(app.url_map)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089)
