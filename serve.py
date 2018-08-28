#!/usr/bin/python 
import sys, os
# working inside the lib
sys.path.append('..')
import cqparts_bucket
import cqparts
from cqparts_bucket import * 
import cqparts.search as cs
from cqparts.display import display

from flask import Flask, jsonify, abort , render_template, request

from anytree import Node , RenderTree , NodeMixin
from anytree.search import findall
from anytree.resolver import Resolver

from collections import OrderedDict
app = Flask(__name__)

class thing(NodeMixin):
    def __init__(self,name,parent=None,**kwargs):
        super(thing,self).__init__()
        self.name = name
        self.built = False
        self.classname = None
        self.parent = parent
        self.params = None
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
                'params' : self.params
            }
        return val 

    def dir(self):
        l = []
        if self.parent != None:
            up  = self.parent.info()
            up['name'] = self.parent.get_path() 
            l.append(up)
        for i in self.children:
            l.append(i.info())
        return l

    def __repr__(self):
        return "<thing: "+self.get_path()+">"

class directory():
    def __init__(self,base,name):
        d = cs.index[name]
        self.d = d
        self.res = Resolver('name')
        self.base = base
        self.class_dict = {}
        self.k = {}
        self.root = thing(base)
        self.build()

    def build(self):
        for i in cs.index.keys():
            p = thing(i,parent=self.root)
            for j in cs.index[i]:
                b = thing(j,parent=p)
                for k in cs.index[i][j]:
                    cn = type(k()).__module__+'.'+k.__name__
                    t = thing(k.__name__,parent=b,c=k,classname=cn)
                    self.class_dict[cn] = t
                    self.k[self.base+'/'+i+'/'+j+'/'+k.__name__] = t

    def children(self,path):
        r = self.res.get(self.root,path)
        print r

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
        app.logger.error("%s",o)
        o.exporter('gltf')('static/cache/'+t.name+'/out.gltf')
        app.logger.error("export finished")

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


#d = directory(cqparts_bucket._namespace,'export')
d = directory('cqparts','export')
print(RenderTree(d.root))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/')
def base():
    return render_template('list.html',items=d.root.dir())

@app.route('/list')
def list():
    return jsonify(d.items())

@app.route('/list/<path:modelname>')
def subcat(modelname):
    return render_template('list.html',items=d.prefix(modelname))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8089)
