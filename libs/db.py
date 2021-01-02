import functools
import os
from .app_logging import use_logging
from .custom_msg import custom_response_msg
from .data_validation import source_already_exist
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = RethinkDB()

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015

DB_NAME = os.environ.get('DB_NAME') or 'git-sources'
TABLE_NAME = os.environ.get('TABLE_NAME') or 'sources'

logging = use_logging()

def db_setup():
    conn = r.connect(RDB_HOST, RDB_PORT)
    try:
        r.db_create(DB_NAME).run(conn)
    except RqlRuntimeError:
        logging.info("Database '{}' already exists".format(DB_NAME))

class db_conn:
    def __init__(self, source_id=None):
        self.id = id

    def __call__(self, func):
        def wrapper(source_id=None, source_data=None):
            logging.info("Database '{}' connected".format(DB_NAME))
            conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
            return func(conn, source_id)
        return wrapper

def create_table():
    try:
        conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
        r.table_create(TABLE_NAME).run(conn)
    except RqlRuntimeError:
        logging.info("Table '{}' already exist".format(TABLE_NAME))

@db_conn(None)
def get_git_sources(conn, source_id=None):
    if source_id:
        return str(source_id)
    else:
        sources = r.table(TABLE_NAME).run(conn)
        return sources

@db_conn(None)
def add_git_source(conn, source_data):
    add_source_success = "Add new source success!"
    add_source_failed = "Add new source failed!"
    duplicated_source = "Source already exist!"

    try:
        sources = [source for source in get_git_sources()]
        if not len(sources):
            source_data['id'] = len(sources) + 1
            r.table(TABLE_NAME).insert(source_data).run(conn)
            logging.info(add_source_success)
            return custom_response_msg(add_source_success, 200)

        for source in sources:
            if not source_already_exist(source, source_data):
                source_data['id'] = len(sources) + 1
                r.table(TABLE_NAME).insert(source_data).run(conn)
                logging.info(add_source_success)
                return custom_response_msg(add_source_success, 200)
            else:
                logging.info(duplicated_source)
                return custom_response_msg(duplicated_source, 200)

    except RqlRuntimeError:
        logging.info(add_source_failed)
        return custom_response_msg(add_source_failed, 500)

@db_conn(None)
def delete_git_source(conn, source_id):
    try:
        r.table(TABLE_NAME).get(source_id).delete().run(conn)
    except RqlRuntimeError:
        msg = "Deleting source failed!"
        return custom_response_msg(msg, 500)
