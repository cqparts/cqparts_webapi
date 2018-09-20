#!/usr/bin/env python
" dump the entire directory to a folder"

# don't run the application but use the templates
from flask import Flask, jsonify, abort, render_template, request, session

# import directory
import inspect
import os
import requests, json
import distutils.dir_util

from client_api import cqparts_api
import directory


#prefix = "/opt/cqparts.github.io/"
prefix = "dump"
github = "http://github.com/zignig/cqparts_bucket/blob/master/"
app = Flask(__name__)
d = directory.Directory("cqparts", "export")
api = cqparts_api()
# grabthe templating environment
j = app.jinja_env


# templates
def make_view(item):
    html = j.get_template("dump_show.html").render(item=item)
    return html


def make_page(item):
    html = j.get_template("dump_list.html").render(dirs=item)
    return html


def make_intro(item):
    html = j.get_template("dump_intro.html").render(dirs=item)
    return html


def make_index(l):
    html = j.get_template("dump_index.html").render(list=l)
    return html


def dir_copy(src, dst):
    distutils.dir_util.copy_tree(src, dst)


def static_files():
    dir_copy("./static/", prefix + os.sep + "static")


def model_files():
    dir_copy("./cache/model", prefix + os.sep + "model")


def img_files():
    dir_copy("./cache/img", prefix + os.sep + "img")


def build():
    unbuilt = api.unbuilt()
    for i in unbuilt:
        path = i["path"]
        api.show(path)
    # copy files into place
    static_files()
    model_files()
    img_files()
    # build the pages
    built = api.all()
    build_pages(built)


# fake wrapper class
class meta_thing:
    def __init__(self, **data):
        self.__dict__.update(data)

    def get_path(self):
        return self.path

    def get_class(self):
        cl = d.get_path(self.get_path())
        return cl.c


def build_pages(l):
    file_list = []
    for j in l:
        i = meta_thing(**j)
        try:
            os.makedirs(prefix + i.get_path())
        except:
            pass
        if i.leaf:
            c = i.get_class()
            line_number = inspect.getsourcelines(c)[1]
            i.github = github + i.classname.split(".")[1] + ".py#L" + str(line_number)
            page = make_view(i)
            f = open(prefix + "/" + i.get_path() + "/index.html", "w")
            f.write(page)
            f.close()
            # fix image path
            i.image_path = "/img/" + i.name + ".png"
            file_list.append(i)
        else:
            # fix the image path
            for k in i.list:
                k["image_path"] = "/img/" + k["name"] + ".png"
            page = make_page(i)
            f = open(prefix + i.get_path() + "/index.html", "w")
            f.write(page)
            f.close()

    # cqparts top directory
    top_list = make_index(file_list)
    f = open(prefix + "/cqparts/index.html", "w")
    f.write(top_list)
    f.close()
    # frontpage
    showcase = api.showcase()
    # fix the image path
    if showcase is not None:
        for k in showcase:
            print(k)
            k["image_path"] = "/img/" + k["name"] + ".png"
            #k["path"] = d.base +"/" + d.name +k["name"]
    else:
        showcase = []
    index = make_intro(showcase)
    f = open(prefix + "/index.html", "w")
    f.write(index)
    f.close()


build()
