#!/usr/bin/env python
import sys, os

sys.path.append("..")

import cqparts_bucket
from cqparts_bucket import *
#from experimental.zignig import *

import cqparts.search as cs
import cqparts
from cqparts.display import display

import json
import zipfile

from anytree import Node, RenderTree, NodeMixin, PreOrderIter
from anytree.search import findall, find_by_attr, findall_by_attr
from anytree.resolver import Resolver

import views
import render
import db
import importer
from thing import thing


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
        self.build_tree("showcase", self.root)
        self.build_other()

        self.alter_build(name)
        self.store = db.Store(prefix=prefix)

    def alter_build(self,name):
        reg = cs.index.copy()
        s = reg[name]
        keys = s.keys()
        for i in keys:
            sub = s[i].copy()
            print(i,sub)

    def build_other(self):
        p = thing("lib", parent=self.root)
        k = list(self.d.keys())
        for i in k:
            self.build_tree(i, p)

    def build_tree(self, name, root):
        print(name,root)
        if name not in self.d:
            return
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
        data["leaf"] = False
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
            self.export(item)
            self.store.upsert(item)

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
        # create the object
        o = t.c(**t.params)
        gltf_path = folder_name + "/out.gltf"
        r = o.exporter("gltf")
        # build the gltf
        v = r(gltf_path)
        view = [r.scene_min, r.scene_max]
        t.view = views.placed(view)
        t.gltf_path = "/" + self.export_prefix + "/" + self.export_path + "/" + t.name

    def set_image(self, imgname):
        name = imgname.split(".")[0]
        t = self.get_name(name)
        if t is not None:
            path = os.sep + self.export_prefix + os.sep + "img" + os.sep
            t.image_path = path + imgname
            t.pending = False
            t.rendered = True
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

    def rerender(self):
        j = self.treeiter('export')
        for i in j:
            if i.is_leaf:
                i.rendered = False

    def stats(self):
        j = self.treeiter('export')
        counter = 0
        build_counter = 0
        render_count = 0
        for i in j:
            if i.is_leaf:
                counter = counter + 1
                if i.built:
                    build_counter = build_counter + 1
                if i.rendered:
                    render_count = render_count + 1
        return { "total":counter ,"built": build_counter,"rendered":render_count}

if __name__ == "__main__":
    d = Directory("examples","export")
