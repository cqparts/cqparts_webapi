# generate the landing page

import yaml
from flask import Flask, jsonify, abort, render_template

import api

def get_landing(app,d,local=True):
    # get the front matter
    sc = []
    l = d.treeiter("export/showcase")
    for i in l:
        if i.is_leaf == True:
            if local:
                i.image_path = "/img/" + i.name + ".png"
            sc.append(i.info())
                
    front = yaml.load(open('inf.yaml').read())
    sections = front['sections']
    tmpl = app.jinja_env
    for i in sections.keys():
        try:
            sec = tmpl.get_template('landing/'+i+'.html')
            sections[i]['data'] = sec.render(list=sc)
        except:
            print(i+' FAILED')
         
    return tmpl.get_template('landing.html').render(data=front) 
    
    
