import os
from flask import g
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = RethinkDB()

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015

DB_NAME = os.environ.get('DB_NAME') or 'git-sources'
TABLE_NAME = os.environ.get('TABLE_NAME') or 'sources'

def connect_to_db(func):
    def wrapper():
        g.logging.info("Connect to Database {}".format(DB_NAME))
        conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
        return func(conn)
    return wrapper

def DBSetup():
    conn = r.connect(RDB_HOST, RDB_PORT)
    try:
        r.db_create(DB_NAME).run(conn)
    except RqlRuntimeError:
        g.logging.info("Database '{}' already exists".format(DB_NAME))

@connect_to_db
def CreateTable(conn):
    try:
        r.table_create(TABLE_NAME).run(conn)
    except RqlRuntimeError:
        g.logging.info("Table '{}' already exist".format(TABLE_NAME))

@connect_to_db
def GetGitSources(conn):
    sources = r.table(TABLE_NAME).run(conn)
    return sources
