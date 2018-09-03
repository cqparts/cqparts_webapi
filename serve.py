#!/usr/bin/env python
import sys, os
# working inside the lib
sys.path.append('..')
import cqparts_bucket
import cqparts
from cqparts_bucket import * 
import cqparts.search as cs
from cqparts.display import display

from flask import Flask, jsonify, abort , render_template, request, session

from anytree import Node , RenderTree , NodeMixin
from anytree.search import findall
from anytree.resolver import Resolver

from collections import OrderedDict

import sqlite3
import api
import cache
import views


class thing(NodeMixin):
    def __init__(self,name,parent=None,**kwargs):
        super(thing,self).__init__()
        self.name = name
        self.built = False
        self.classname = None
        self.parent = parent
        self.params = {} 
        self.doc = "NoDoc"
        self.gltf_path = ""
        self.view = [[1,1,1],[0,0,0]]
        self.__dict__.update(kwargs)

    def get_path(self):
        args = "%s" % self.separator.join([""] + [str(node.name) for node in self.path])
        return str(args)

    def info(self):
        val = {
                'path':self.get_path(),
                'name':self.name,
                'leaf': self.is_leaf,
                'built': self.built,
                'classname' : self.classname,
                'params' : self.params,
                'doc' : self.doc,
                'view' : self.view,
                'gltf_path' : self.gltf_path,
            }
        if self.parent is not None:
            val['parent'] = self.parent.get_path()
        return val 

    def dir(self):
        data = {}
        if self.parent != None:
            data['parent'] = self.parent.get_path() 
        l = []
        for i in self.children:
            l.append(i.info())
        data['list'] = l 
        data['path'] = self.get_path()
        return data 

    def __repr__(self):
        return "<thing: "+self.get_path()+","+str(self.classname)+">"

class directory():
    def __init__(self,base,name,database,export="static/cache"):
        self.database = database
        self.name = name
        self.d = cs.index.copy()
        self.res = Resolver('name')
        self.base = base
        self.class_dict = {}
        self.k = {}
        self.export_part = export
        self.root = thing(base)
        self.build_tree(name,self.root)
        self.build_other()

    def build_other(self):
        p = thing('lib',parent=self.root)
        k = self.d.keys()
        print k
        for i in k:
            self.build_tree(i,p)

    def build_tree(self,name,root):
        p = thing(name,parent=root)
        tr = self.d.pop(name)
        for j in tr:
            b = thing(j,parent=p)
            for k in tr[j]:
                cn = type(k()).__module__+'.'+k.__name__
                t = thing(k.__name__,parent=b,c=k,classname=cn,doc=k.__doc__)
                self.class_dict[cn] = t
                self.k[self.base+'/'+self.name+'/'+j+'/'+k.__name__] = t

    def children(self,path):
        r = self.res.get(self.root,path)
        return r

    def exists(self,key):
        if key in self.k:
            return True
        return False

    def prefix(self,key):
        v = self.res.get(self.root,'/'+key)
        return v.dir()

    def build_part(self,params):
        key = params.pop('classname',None)
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

    def export(self,t):
        try:
            os.removedirs('static/cache/'+t.name)
        except:
            pass
        try:
            os.makedirs('static/cache/'+t.name)
        except:
            pass
        o = t.c(**t.params)
        gltf_path = 'static/cache/'+t.name+'/out.gltf'
        r =  o.exporter('gltf')
        v = r(gltf_path)
        view = [r.scene_min,r.scene_max]
        t.view = views.placed(view)
        app.logger.error("%s %s",view,views.placed(view))

        t.gltf_path = gltf_path

    def params(self,key):
        if self.exists(key) == False:
            abort(404)
        t = self.k[key]
        d = {}
        if t.built == False:
            inst = t.c() 
            pi = inst.params().items()
            for i in pi:
                # only grab the floats for now
                if isinstance(i[1],float):
                    d[i[0]] = i[1]
                if isinstance(i[1],int):
                    d[i[0]] = i[1]
            t.params = d
            self.export(t)
            t.built = True
        info = t.info()
        return info 


db = sqlite3.connect("meta.db")
app = Flask(__name__)
app.secret_key = "sort of but not actually that secret"
app.register_blueprint(api.bp)
app.register_blueprint(cache.cachebp)
d = directory('cqparts','export',db)
api.d = d 
print(RenderTree(d.root))

# don't cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
#    app.logger.error(session)
    return response

@app.route('/')
def base():
    session['bork'] = True
    return render_template('list.html',dirs=d.prefix(d.base))

@app.route('/list/<path:modelname>')
def subcat(modelname):
    return render_template('list.html',dirs=d.prefix(modelname))

@app.route('/show/<path:modelname>',methods=['GET','POST'])
def show_model(modelname):
    if request.method == 'POST':
        v = request.form.copy()
        d.build_part(v)
    ob = d.params(modelname)
    return render_template('view.html',item=d.params(modelname))

@app.route('/rebuild',methods=['POST'])
def rebuild():
    return jsonify(request.form.items())

print(app.url_map)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8089)
