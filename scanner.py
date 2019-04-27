#!/usr/bin/python2
" scanning all objects "

import directory
import inspect
import db

d = directory.Directory("examples", "export")

l = d.treeiter("/examples/export")

files = {}
for i in l:
    # s.upsert(i)
    #print(i)
    d.store.upsert(i)
    if i.is_leaf:
        name = i.name
        #print(i.info())
        #c = inspect.getmro(i.c)
        print(name)
        #for i in c:
        #    print("\t"+str(i))
        #file_name = inspect.getsourcefile(i.c)
	#print(file_name)
        #files[file_name] = ''
        #line_number = inspect.getsourcelines(i.c)[1]
        # print(name, file_name, line_number)
        # i.image_path = "/cache/img/" + i.name + ".png"
        # d.store.upsert(i)

for i in files:
    print(i)
