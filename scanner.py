" scanning all objects "

import directory
import inspect
import db

s = db.Store()

d = directory.Directory("cqparts", "export")

l = d.treeiter("/cqparts/export")

for i in l:
    # s.upsert(i)
    if i.is_leaf:
        name = i.name
        file_name = inspect.getsourcefile(i.c)
        line_number = inspect.getsourcelines(i.c)[1]
        # print(name, file_name, line_number)

s.list()
