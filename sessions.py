" session holder "

import uuid

class Session:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = "" 
        

class SessionCollection:
    def __init__(self,store):
        self.sessions = {}
        self.store = store

    def get(self,uuid):
        if str(uuid) in self.sessions:
            s = self.sessions[str(uuid)]
            return s
        else:
            s = Session()
            self.sessions[str(s.uuid)] = s
            self.store.new_session(s)
            return s

    def new(self):
        s = Session()
        self.sessions[str(s.uuid)] = s
        self.store.new_session(s)
        return s
        
