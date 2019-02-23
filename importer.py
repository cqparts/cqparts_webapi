"""

Alternate importer for designs

"""

import cqparts.search  as cs
from importlib import import_module
import sys, os
from cqparts.search import register

class meta:
    pass

sys.path.append("..")
class importotron:
    def __init__(self,mods):
        self.mods = mods
        base = meta()
        for i in self.mods:
            try:
                m = import_module(i)
                print("importing "+i)
                setattr(base,i,m)
                if hasattr(m,"__all__"):
                    l = m.__all__
                    for j in l:
                        try:
                            r = import_module(i+'.'+j)
                            print(i,j,m)
                        except:
                            print("fail on "+j)
            except:
                print("module fail ",i)
        self.base = base


mods = [ 'borken' , 'cqparts_bucket' , 'experimental' ]

if __name__ == "__main__":
    im = importotron(mods)
