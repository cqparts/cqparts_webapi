#!/usr/bin/python2
" dump the entire directory to a folder"

# don't run the application but use the templates
from flask import Flask, jsonify, abort, render_template, request, session

# import directory
import inspect
import os
import yaml
import requests, json
import distutils.dir_util

import datetime
from client_api import cqparts_api
import directory
import landing



prefix = "/tmp/hugo"
#prefix = "dump"
github = "http://github.com/zignig/cqparts_bucket/blob/master/"
app = Flask(__name__)
d = directory.Directory("examples", "export")
api = cqparts_api()
# grabthe templating environment
j = app.jinja_env
# custom menu later
data = None

# templates
def make_view(item):
    html = j.get_template("dump/show.html").render(item=item,data=data)
    return html

class tz(datetime.tzinfo):
    def __init__(self):
        self.stdoffset = datetime.timedelta(hours=8)
    def utcoffset(self,dt):
        return datetime.timedelta(hours=8)
    def dst(self, dt):
        # a fixed-offset class:  doesn't account for DST
        return datetime.timedelta(0)

def make_md(item):
    html = j.get_template("dump/hugo_export.md").render(item=item,data=data)
    return html

def make_page(item):
    html = j.get_template("dump/list.html").render(dirs=item,data=data)
    return html


def make_intro():
    return landing.get_landing(app,d) 


def make_index(l):
    html = j.get_template("dump/index.html").render(list=l,data=data)
    return html


def dir_copy(src, dst):
    distutils.dir_util.copy_tree(src, dst)


def static_files():
    dir_copy("./static/", prefix + os.sep + "static")


def model_files():
    dir_copy("./cache/model", prefix + os.sep + "model")


def img_files():
    dir_copy("./cache/img", prefix + os.sep + "img")


def build(f,prefix):
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
    f(built,prefix)

def hugo(prefix):
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
    hugo_pages(built,prefix)


# fake wrapper class
class meta_thing:
    def __init__(self, **data):
        self.__dict__.update(data)

    def get_path(self):
        return self.path

    def get_class(self):
        cl = d.get_path(self.get_path())
        return cl.c


def hugo_pages(l,prefix):
    file_list = []
    for j in l:
        i = meta_thing(**j)
        try:
            os.makedirs(prefix + i.get_path())
        except:
            pass
        if i.leaf:
            if hasattr(i,'name'):
                fp = prefix + os.sep + i.get_path() + os.sep
                sc = inspect.getsourcefile(i.get_class())
                st = os.stat(sc)
                ts = st.st_mtime
                c = datetime.datetime.utcfromtimestamp(ts)
                i.date = c  
                i.image_path = "./cache/img/" + i.name + ".png"
                distutils.file_util.copy_file('./cache/img/'+i.name+".png",fp + i.name + '.png')
                page = make_md(i)
                f = open(fp + "index.md", "w")
                f.write(page)
                f.close()
                # fix image path
                file_list.append(i)
            else:
                print(">>"+j)
        else:
            print(i,j)
        

def build_pages(l,prefix):
    file_list = []
    for j in l:
        i = meta_thing(**j)
        try:
            os.makedirs(prefix + i.get_path())
        except:
            pass
        if i.leaf:
            print(i.name)
            c = i.get_class()
            try:
                line_number = inspect.getsourcelines(c)[1]
            except:
                print('no source')
            i.github = github + i.classname.split(".")[1] + ".py#L" + str(line_number)
            page = make_page(i)
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
    f = open(prefix + "/"+ d.base +"/index.html", "w")
    f.write(top_list)
    f.close()
    # landing page
    index = make_intro()
    f = open(prefix + "/index.html", "w")
    f.write(index)
    f.close()

if __name__ == "__main__":
    #build(build_pages,"/opt/cqparts.github.io")
    build(hugo_pages,"/opt/website/content/thing")
