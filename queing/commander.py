#!/usr/bin/python
from cmd import Cmd
class MyPrompt(Cmd):
   prompt = ">>"
   def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True

   def do_set(self,inp):
       setattr(self,'do_'+inp,self.do_add)

   def do_load(self,inp):
       print(inp)

   def complete_load(self,text,line,begidx,endidx):
       print(text,line,begidx,endidx)

   def do_add(self, inp):
        print("Adding '{}'".format(inp))

   def help_add(self):
       print("Add a new entry to the system.")

   def get_names(self):
       return dir(self)

a = MyPrompt()
a.cmdloop()
