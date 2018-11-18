#!/usr/bin/env python
import sys, os

sys.path.append("..")

#import cqparts_bucket
from cqparts_bucket import *
from experimental.zignig import *

import cqparts.search as cs
import cqparts
from cqparts.display import display

import json
import zipfile

from anytree import Node, RenderTree, NodeMixin, PreOrderIter

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

