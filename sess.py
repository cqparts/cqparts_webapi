" session holder "

import uuid
from flask.sessions import SecureCookieSessionInterface , SessionMixin , SecureCookieSession

# override the session interface for database interface

class SessionCollection(SecureCookieSessionInterface):
    session_class = SecureCookieSession
    def __init__(self,store):
        self.sessions = {}
        self.store = store

    def open_session(self,app,request):
        return self.session_class() 

    def save_session(self,app,session,response):
        super(SessionCollection,self).save_session(app,session,response)
        app.logger.error(session['id'])


    def get(self,uuid):
        if str(uuid) in self.sessions:
            s = self.sessions[str(uuid)]
            return s
        else:
            s = Session()
            self.sessions[str(s.uuid)] = s
            #self.store.new_session(s)
            return s

    def new(self):
        s = Session()
        self.sessions[str(s.uuid)] = s
        self.store.new_session(s)
        return s
        
