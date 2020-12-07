import functools
import os
from .app_logging import use_logging
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = RethinkDB()

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015

DB_NAME = os.environ.get('DB_NAME') or 'git-sources'
TABLE_NAME = os.environ.get('TABLE_NAME') or 'sources'

logging = use_logging()

def DBSetup():
    conn = r.connect(RDB_HOST, RDB_PORT)
    try:
        r.db_create(DB_NAME).run(conn)
    except RqlRuntimeError:
        logging.info("Database '{}' already exists".format(DB_NAME))

class DBConn:
    def __init__(self, source_id=None):
        self.id = id

    def __call__(self, func):
        def wrapper(source_id=None):
            logging.info("Database '{}' connected".format(DB_NAME))
            conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
            return func(conn, source_id)
        return wrapper

def CreateTable():
    try:
        conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
        r.table_create(TABLE_NAME).run(conn)
    except RqlRuntimeError:
        logging.info("Table '{}' already exist".format(TABLE_NAME))

@DBConn(None)
def GetGitSources(conn, source_id=None):
    sources = r.table(TABLE_NAME).run(conn)
    return sources

@DBConn(None)
def DeleteGitSource(conn, source_id):
    try:
        r.table(TABLE_NAME).get(source_id).delete().run(conn)
    except RqlRuntimeError:
        logging.info("Delete failed!")
