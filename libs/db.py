import functools
import os
from .app_logging import use_logging
from .custom_msg import custom_msg_dict, custom_response_msg
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
    def __init__(self):
        pass

    def __call__(self, func):
        def wrapper(source_id=None, source_data=None):
            logging.info("Database '{}' connected".format(DB_NAME))
            conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
            return func(conn, source_id, source_data)
        return wrapper

def create_table():
    try:
        conn = r.connect(RDB_HOST, RDB_PORT, DB_NAME)
        r.table_create(TABLE_NAME).run(conn)
    except RqlRuntimeError:
        logging.info("Table '{}' already exist".format(TABLE_NAME))

@db_conn()
def get_git_sources(conn, source_id=None, source_data=None):
    if source_id:
        source = r.table(TABLE_NAME).get(source_id).run(conn) or {}
        return source
    else:
        sources = sorted([source for source in r.table(TABLE_NAME).run(conn)], key=lambda x: x['id'])
        return sources

@db_conn()
def add_git_source(conn, source_data, source_id=None):
    def add_new_source():
        sources_length = len(sources)
        if sources_length == 0:
            source_data['id'] = 1
        else:
            source_data['id'] = sources[sources_length-1]['id'] + 1

        r.table(TABLE_NAME).insert(source_data).run(conn)
        return custom_response_msg(custom_msg_dict['add_source_success'], 200)

    try:
        sources = [source for source in get_git_sources()]
        if not len(sources):
            return add_new_source()

        if source_already_exist(sources, source_data):
            return custom_response_msg(custom_msg_dict['duplicated_source'], 200)
        else:
            return add_new_source()

    except RqlRuntimeError:
        return custom_response_msg(custom_msg_dict['add_source_failed'], 500)

@db_conn()
def update_git_source(conn, source_id, source_data):
    try:
        if get_git_sources(source_id):
            r.table(TABLE_NAME).filter(r.row['id'] == source_id).update(source_data).run(conn)
            return custom_response_msg(custom_msg_dict['update_source_success'], 200)
        else:
            return custom_response_msg(custom_msg_dict['source_doesnt_exist'], 200)
    
    except RqlRuntimeError:
        return custom_response_msg(custom_msg_dict['update_source_failed'], 500)


@db_conn()
def delete_git_source(conn, source_id, source_data=None):
    try:
        r.table(TABLE_NAME).get(source_id).delete().run(conn)
        return custom_response_msg(custom_msg_dict['delete_source_success'], 200)

    except RqlRuntimeError:
        return custom_response_msg(custom_msg_dict['delete_source_failed'], 500)
