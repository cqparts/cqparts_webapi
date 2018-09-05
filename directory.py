#!/usr/bin/env python
import sys, os

# working inside the lib
sys.path.append("..")
import cqparts_bucket
import cqparts
from cqparts_bucket import *
import cqparts.search as cs
from cqparts.display import display

import json

from anytree import Node, RenderTree, NodeMixin, PreOrderIter
from anytree.search import findall
from anytree.resolver import Resolver

import views
import render


class thing(NodeMixin):
    def __init__(self, name, parent=None, **kwargs):
        super(thing, self).__init__()
        self.name = name
        self.built = False
        self.classname = None
        self.parent = parent
        self.params = {}
        self.doc = "NoDoc"
        self.gltf_path = ""
        self.view = [[1, 1, 1], [0, 0, 0]]
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
        }
        if self.parent is not None:
            val["parent"] = self.parent.get_path()
        return val

    def dir(self):
        data = {}
        if self.parent != None:
            data["parent"] = self.parent.get_path()
        l = []
        for i in self.children:
            l.append(i.info())
        data["list"] = l
        data["path"] = self.get_path()
        return data

    def __repr__(self):
        return "<thing: " + self.get_path() + "," + str(self.classname) + ">"


class Directory:
    def __init__(self, base, name, prefix="static", export="cache"):
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

    def build_other(self):
        p = thing("lib", parent=self.root)
        k = self.d.keys()
        print(k)
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
                self.k[self.base + "/" + self.name + "/" + j + "/" + k.__name__] = t

    def get_path(self, path):
        r = self.res.get(self.root, path)
        return r

    def exists(self, key):
        if key in self.k:
            return True
        return False

    def prefix(self, key):
        v = self.res.get(self.root, "/" + key)
        return v.dir()

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
        t.render(render.event)

    def params(self, key):
        if self.exists(key) == False:
            print(str(key) + "keyfail") 
            print(self.k.keys())
        t = self.k[key]
        d = {}
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
        info = t.info()
        return info

    def treeiter(self, key):
        nodes = []
        item = self.get_path(key)
        for node in PreOrderIter(item):
            nodes.append(node)
        return nodes
