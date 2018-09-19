#!/usr/bin/env python
" scanning all objects "

import directory
import inspect
import db

d = directory.Directory("cqparts", "export")

l = d.treeiter("/cqparts/export")

for i in l:
    # s.upsert(i)
    print(i)
    d.store.upsert(i)
    if i.is_leaf:
        name = i.name
        print(i.info())
        file_name = inspect.getsourcefile(i.c)
        line_number = inspect.getsourcelines(i.c)[1]
        # print(name, file_name, line_number)
        # i.image_path = "/cache/img/" + i.name + ".png"
        # d.store.upsert(i)
