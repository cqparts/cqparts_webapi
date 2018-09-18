#!/usr/bin/env python
import sys, os

sys.path.append("..")

import cqparts_bucket
import cqparts
from cqparts_bucket import *
import cqparts.search as cs
from cqparts.display import display

import json
import zipfile

from anytree import Node, RenderTree, NodeMixin, PreOrderIter
from anytree.search import findall, find_by_attr, findall_by_attr
from anytree.resolver import Resolver

import views
import render
import db


class thing(NodeMixin):
    def __init__(self, name, parent=None, **kwargs):
        super(thing, self).__init__()
        self.name = name
        self.loaded = False  # gret from sql or create
        self.built = False
        self.rendered = False
        self.classname = None
        self.parent = parent
        self.params = {}
        self.doc = "NoDoc"
        self.gltf_path = ""
        self.image_path = ""
        self.view = {}
        self._hidden = ""
        self.__dict__.update(kwargs)

    def get_path(self):
        args = "%s" % self.separator.join([""] + [str(node.name) for node in self.path])
        return str(args)

    def render(self, event):
        val = {
            "name": self.name,
            "cam": self.view["cam"],
            "target": self.view["target"],
        }
        event.append("event:render\n")
        r = "data:" + json.dumps(val) + "\n"
        event.append(r)
        event.append("\n")

    def info(self):
        val = {
            "path": self.get_path(),
            "name": self.name,
            "leaf": self.is_leaf,
            "built": self.built,
            "classname": self.classname,
            "params": self.params,
            "doc": self.doc,
            "view": self.view,
            "gltf_path": self.gltf_path,
            "loaded": self.loaded,
            "image_path": self.image_path,
        }
        if self.parent is not None:
            val["parent"] = self.parent.get_path()
        return val

    def dir(self):
        val = {
            "path": self.get_path(),
            "leaf": self.is_leaf,
            "built": self.built,
            "name": self.name,
            "image_path": self.image_path,
        }
        return val

    def __repr__(self):
        return "<thing: " + self.get_path() + "," + str(self.classname) + ">"


class Directory:
    def __init__(self, base, name, prefix="cache", export="model"):
        self.name = name
        self.d = cs.index.copy()
        self.res = Resolver("name")
        self.base = base
        self.class_dict = {}
        self.k = {}
        self.export_path = export
        self.export_prefix = prefix
        self.root = thing(base)
        self.build_tree(name, self.root)
        self.build_other()

        self.store = db.Store(prefix=prefix)

    def build_other(self):
        p = thing("lib", parent=self.root)
        k = self.d.keys()
        for i in k:
            self.build_tree(i, p)

    def build_tree(self, name, root):
        p = thing(name, parent=root)
        tr = self.d.pop(name)
        for j in tr:
            b = thing(j, parent=p)
            for k in tr[j]:
                cn = type(k()).__module__ + "." + k.__name__
                t = thing(k.__name__, parent=b, c=k, classname=cn, doc=k.__doc__)
                self.class_dict[cn] = t
                self.k[p.get_path() + "/" + j + "/" + k.__name__] = t

    def get_path(self, path):
        r = self.res.get(self.root, path)
        return r

    def get_name(self, name):
        n = findall_by_attr(self.root, name)
        return n[0]

    def exists(self, key):
        if "/" + key in self.k:
            return True
        return False

    def prefix(self, key):
        v = self.res.get(self.root, "/" + key)
        data = {}
        if v.parent != None:
            data["parent"] = v.parent.get_path()
        l = []
        for i in v.children:
            if i.loaded == False:
                self.store.fetch(i)
            l.append(i.dir())
        data["list"] = l
        data["name"] = v.name
        data["path"] = v.get_path()
        return data

    def build_part(self, params):
        key = params.pop("classname", None)
        if key in self.class_dict:
            fixes = {}
            for i in params:
                try:
                    fixes[i] = float(params[i])
                except:
                    pass
            item = self.class_dict[key]
            item.params.update(fixes)
            item.rendered = False
            self.store.upsert(item)
            self.export(item)

    def export(self, t):
        folder_name = self.export_prefix + "/" + self.export_path + "/" + t.name
        try:
            os.removedirs(folder_name)
        except:
            pass
        try:
            os.makedirs(folder_name)
        except:
            pass
        o = t.c(**t.params)
        gltf_path = folder_name + "/out.gltf"
        r = o.exporter("gltf")
        v = r(gltf_path)
        view = [r.scene_min, r.scene_max]
        t.view = views.placed(view)
        t.gltf_path = "/" + self.export_path + "/" + t.name + "/out.gltf"
        # t.render(render.event)

    def set_image(self, imgname):
        name = imgname.split(".")[0]
        t = self.get_name(name)
        if t is not None:
            path = (
                os.sep
                + self.export_prefix
                + os.sep
                + self.export_path
                + os.sep
                + "img"
                + os.sep
            )
            t.image_path = path + imgname
            self.store.upsert(t)

    def fetch(self, t):
        self.store.fetch(t)
        # due to multiple export paths (for dumping)
        # this is set by itself
        t.gltf_path = "/" + self.export_prefix + "/" + self.export_path + "/" + t.name

    def params(self, key):
        if self.exists(key) == False:
            print(str(key) + "keyfail")
            print(self.k.keys())
        t = self.k["/" + key]
        d = {}
        if t.loaded == False:
            self.fetch(t)
        if t.built == False:
            inst = t.c()
            pi = inst.params().items()
            for i in pi:
                # only grab the floats for now
                if isinstance(i[1], float):
                    d[i[0]] = i[1]
                if isinstance(i[1], int):
                    d[i[0]] = i[1]
            t.params = d
            self.export(t)
            t.built = True
            t.rendered = False
            self.store.upsert(t)
        info = t.info()
        return info

    def get_zipped(self, t):
        r = self.export_prefix + os.sep + self.export_path + os.sep + t.name + os.sep
        export_folder = self.export_prefix + os.sep + "zip"
        zip_file = export_folder + os.sep + t.name + ".zip"
        f = os.listdir(r)
        try:
            os.makedirs(export_folder)
        except:
            pass
        z = zipfile.ZipFile(zip_file, "w")
        for i in f:
            z.write(r + i, t.name + os.sep + i)
        z.close()
        return zip_file

    def treeiter(self, key):
        nodes = []
        item = self.get_path(key)
        for node in PreOrderIter(item):
            if node.loaded == False:
                self.fetch(node)
            nodes.append(node)
        return nodes
