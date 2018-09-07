#!/usr/bin/env python
" dump the entire directory to a folder"

# don't run the application but use the templates
from flask import Flask, jsonify, abort, render_template, request, session

import directory
import inspect
import os

prefix = "dump"
github = "http://github.com/zignig/cqparts_bucket/blob/master/"
app = Flask(__name__)
d = directory.Directory("cqparts", "export", prefix=prefix, export="model")

# grabthe templating environment
j = app.jinja_env


def make_view(item):
    html = j.get_template("show.html").render(item=item)
    return html


def make_index(l):
    html = j.get_template("dump_index.html").render(list=l)
    return html


l = d.treeiter("/cqparts/export")

file_list = []
for i in l:
    if i.is_leaf:
        d.params(i.info()["path"][1:])
        info = i.info()
        # print(i.name,i.get_path())
        # os.makedirs(prefix + "/" + i.get_path())
        line_number = inspect.getsourcelines(i.c)[1]
        info["github"] = github + i.classname.split(".")[1] + ".py#L" + str(line_number)
        page = make_view(info)
        f = open(prefix + "/" + i.name + ".html", "w")
        f.write(page)
        f.close()

        flist = {"name": i.name, "page": i.name + ".html"}
        file_list.append(flist)


index = make_index(file_list)
f = open(prefix + "/index.html", "w")
f.write(index)
f.close()
