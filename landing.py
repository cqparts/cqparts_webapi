# generate the landing page

import yaml
from flask import Flask, jsonify, abort, render_template

def get_landing(app):
    # get the front matter
    front = yaml.load(open('inf.yaml').read())
    sections = front['sections']
    tmpl = app.jinja_env
    for i in sections.keys():
        try:
            a = tmpl.get_template('landing/'+i+'.html')
            print(i+' got template')
        except:
            print(i+' FAILED')
         
    return str(sections)
    
    
