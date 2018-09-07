#!/usr/bin/env python
" rebuild  the directory"


import directory
import inspect
import os

d = directory.Directory("cqparts", "export")

l = d.treeiter("/cqparts/export")
for i in l:
    if i.is_leaf:
        print(i.name)
        d.params(i.info()["path"][1:])
        i.built = true
        d.store.upsert(i)
