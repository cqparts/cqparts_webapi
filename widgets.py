# generate the landing page

from flask import Flask, jsonify, abort, render_template

d = None

def front(app):
    data = []     
    tmpl = app.jinja_env
    widgets = {
        'showcase' : showcase(app),
        'stats' : stats(app),
        'links' : links(app),
    }
    return tmpl.get_template('front.html').render(widgets=widgets,data=data) 
    
    
def links(app):
    return app.jinja_env.get_template('widgets/links.html').render() 

def stats(app):
    data = d.stats()
    return app.jinja_env.get_template('widgets/stats.html').render(data=data) 

def showcase(app):
    sc = []
    l = d.treeiter("export/showcase")
    for i in l:
        if i.is_leaf == True:
            sc.append(i.info())
    return app.jinja_env.get_template('widgets/showcase.html').render(list=sc) 
