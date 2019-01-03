__all__ = ['click']

# from 
# http://martyalchin.com/2008/jan/10/simple-plugin-framework/

from .start import ActionProvider , PluginMount        

def list():
    return ActionProvider.plugins

import os 
from os.path import dirname

basedir = dirname(__file__)
l = os.listdir(basedir)
for i in l:
    if i.endswith('.py'):
        if not i.startswith('_') and ( not i.startswith('start') ):
            try:
                n = i.split('.')[0]
                __import__(__name__+"."+n)
                print(n)
            except Exception as e :
                print("FAIL ",i,e)

