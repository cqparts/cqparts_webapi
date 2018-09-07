"database layer"

from sqlalchemy import *
from sqlalchemy.sql import and_, or_, not_

# from directory import thing
import json
import os

# environmental variable so it does not get published
# should be in the form
# postgresql+psycopg2://user:password@host/database
sql_string = os.environ["CQPARTS_DB"]


class Store:
    def __init__(self, prefix="cache"):
        self.db = create_engine(sql_string)
        self.metadata = MetaData()
        self.prefix = prefix
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
        self.metadata.create_all(self.db)
        self.conn = self.db.connect()

    def list(self):
        s = select([self.things])
        result = self.conn.execute(s)
        for row in result:
            print(row)

    def fetch(self, t):
        s = select([self.things.c.jsondata]).where(
            and_(
                self.things.c.classname == t.classname,
                self.things.c.prefix == self.prefix,
            )
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
            t.image_path = data["image_path"]

    def upsert(self, t):
        s = select([func.count(self.things.c.id)]).where(
            and_(
                self.things.c.classname == t.classname,
                self.things.c.prefix == self.prefix,
            )
        )
        res = self.conn.execute(s)
        exists = res.fetchone()[0]
        jsdata = json.dumps(t.info())
        if exists == 0:
            ins = self.things.insert()
            self.conn.execute(
                ins,
                prefix=self.prefix,
                classname=t.classname,
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
            self.conn.execute(upd, name=t.name, jsondata=jsdata)
