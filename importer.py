"""

Alternate importer for designs 

"""

from importlib import import_module
import sys, os

sys.path.append("..")
class importotron:
    def __init__(self,mods):
        self.mods = mods
        for i in self.mods:
            try:
                m = import_module(i)
                print("importing "+i)
                if hasattr(m,"__all__"):
                    l = m.__all__
                    for j in l:
                        print(i,j)
            except:
                print("fail on "+i)


mods = [ 'borken' , 'cqparts_bucket' , 'experimental' ]

i = importotron(mods)

