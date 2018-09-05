"database layer"

from sqlalchemy import *

# from directory import thing
import json
import os

sql_string = os.environ["CQPARTS_DB"]


class Store:
    def __init__(self, name="meta.db"):
        # self.db = create_engine("sqlite:///meta.db")
        self.db = create_engine(sql_string)
        self.metadata = MetaData()
        self.things = Table(
            "things",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("classname", String),
            Column("path", String),
            Column("name", String),
            Column("jsondata", String),
        )
        self.metadata.create_all(self.db)
        self.conn = self.db.connect()

    def list(self):
        s = select([self.things])
        result = self.conn.execute(s)
        for row in result:
            print(row)

    def fetch(self, t):
        s = select([self.things.c.jsondata]).where(
            self.things.c.classname == t.classname
        )
        res = self.conn.execute(s)
        row = res.fetchone()
        if row is not None:
            t.loaded = True
            # just grab a few things fornow
            data = json.loads(row[0])
            t.built = data["built"]
            t.view = data["view"]
            t.params = data["params"]
        else:
            self.upsert(t)

    def upsert(self, t):
        s = select([func.count(self.things.c.id)]).where(
            self.things.c.classname == t.classname
        )
        res = self.conn.execute(s)
        exists = res.fetchone()[0]
        jsdata = json.dumps(t.info())
        if exists == 0:
            ins = self.things.insert()
            self.conn.execute(ins, classname=t.classname, name=t.name, jsondata=jsdata)
        else:
            upd = self.things.update().where(self.things.c.classname == t.classname)
            self.conn.execute(upd, name=t.name, jsondata=jsdata)
