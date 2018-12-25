"database layer"

from sqlalchemy import *
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.types import Binary
from sqlalchemy.types import TypeDecorator 

# from directory import thing
import json
import os

# environmental variable so it does not get published
# should be in the form
# postgresql+psycopg2://user:password@host/database
# or use sqlite3 
# 'sqlite:///path/data.db'
sql_string = os.environ["CQPARTS_DB"]


class Store:
    def __init__(self, prefix="cache"):
        self.db = create_engine(sql_string)
        self.metadata = MetaData()
        self.prefix = prefix

        self.thing_table()
        self.session_table()
        self.sizes_table()

        self.metadata.create_all(self.db)


    def sizes_table(self):
        self.rendersizes = Table(
            "rendersizes",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("width", Integer),
            Column("height", Integer),
            Column("samples", Integer),
        )

    def get_sizes(self):
        conn = self.db.connect()
        s = select([self.rendersizes])
        result = conn.execute(s)
        sizes = []
        for row in result:
            sizes.append({
                "id" : row.id,
                "width" : row.width,
                "height" : row.height,
                "samples" : row.samples,
            })
        return sizes

    def thing_table(self):
        self.things = Table(
            "things",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("classname", String),
            Column("prefix", String),
            Column("path", String),
            Column("name", String),
            Column("jsondata", String),
            Column("render", Boolean),
            Column("built", Boolean),
        )

    def session_table(self):
        self.sessions = Table(
            "sessions",
            self.metadata,
            Column("id",String,primary_key=True),
            Column("name",String),
        )

    def new_session(self,s):
        conn = self.db.connect()
        ins = self.sessions.insert()
        conn.execute(
            ins,
            id= s.uuid,
            name = s.name
        )

    def get_session(self,s):
        conn = self.db.connect()
        s = select(self.sessions).where( self.sessions.uuid == str(s.uuid) )
        result = conn.execute(s)
        return result     

    def list(self):
        s = select([self.things])
        conn = self.db.connect()
        result = conn.execute(s)
        for row in result:
            print(row)

    def fetch(self, t):
        s = select([self.things.c.jsondata]).where(
            and_(
                self.things.c.classname == t.classname,
                self.things.c.prefix == self.prefix,
            )
        )
        conn = self.db.connect()
        res = conn.execute(s)
        row = res.fetchone()
        if row is not None:
            t.loaded = True
            # just grab a few things fornow
            data = json.loads(row[0])
            t.built = data["built"]
            t.view = data["view"]
            t.params = data["params"]
            t.rendered = data["rendered"]
            t.image_path = data["image_path"]
            t.gltf_path = data["gltf_path"]

    def upsert(self, t):
        s = select([func.count(self.things.c.id)]).where(
            and_(
                self.things.c.classname == t.classname,
                self.things.c.prefix == self.prefix,
            )
        )
        conn = self.db.connect()
        res = conn.execute(s)
        exists = res.fetchone()[0]
        jsdata = json.dumps(t.info())
        if exists == 0:
            ins = self.things.insert()
            conn.execute(
                ins,
                prefix=self.prefix,
                classname=t.classname,
                built=t.built,
                name=t.name,
                jsondata=jsdata,
                render=t.rendered,
            )
        else:
            upd = self.things.update().where(
                and_(
                    self.things.c.classname == t.classname,
                    self.things.c.prefix == self.prefix,
                )
            )
            conn.execute(upd, built=t.built, render=t.rendered,name=t.name, jsondata=jsdata)
