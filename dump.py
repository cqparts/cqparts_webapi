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
d = directory.Directory("cqparts", "export") #, prefix=prefix, export="model")

# grabthe templating environment
j = app.jinja_env


def make_view(item):
    html = j.get_template("dump_show.html").render(item=item)
    return html

def make_page(item):
    html = j.get_template("dump_list.html").render(dirs=item)
    return html

def make_index(l):
    html = j.get_template("dump_index.html").render(list=l)
    return html


l = d.treeiter("/cqparts/export")

file_list = []
for i in l:
    info = i.info()
    #print(i,info)
    if i.is_leaf:
        #print(i.name,i.get_path())
        d.params(i.info()["path"][1:])
        try:
            os.makedirs(prefix + "/" + i.get_path())
        except:
            pass
        line_number = inspect.getsourcelines(i.c)[1]
        info["github"] = github + i.classname.split(".")[1] + ".py#L" + str(line_number)
        page = make_view(info)
        f = open(prefix + "/" + i.get_path() + "/index.html", "w")
        f.write(page)
        f.close()

        flist = {"name": i.name, "page": i.name + ".html"}
        file_list.append(flist)
    else:
        modelname = i.get_path()[1:]
        print(modelname)
        dirs = d.prefix(modelname)
        page = make_page(dirs)
        f = open(prefix + "/" + i.get_path() + "/index.html", "w")
        f.write(page)
        f.close()

index = make_index(file_list)
f = open(prefix + "/index.html", "w")
f.write(index)
f.close()
