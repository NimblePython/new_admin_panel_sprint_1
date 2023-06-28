import pytest
import os
import sqlite3

from dotenv import load_dotenv
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()


@pytest.fixture(scope='module')
def load_env():
    lite_db_path = os.environ.get('DB_NAME_LITE')
    pg_db = os.environ.get('DB_NAME_PG')
    usr = os.environ.get('DB_USER')
    pwd = os.environ.get('DB_PASSWORD')
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT'))

    return {'lite_db_path': lite_db_path,
            'pg_db': pg_db,
            'usr': usr,
            'pwd': pwd,
            'host': host,
            'port': port,
            }

"""
@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()
"""


@pytest.fixture(scope="module")
def lite_conn(load_env):
    conn = sqlite3.connect(load_env['lite_db_path'])
    conn.row_factory = sqlite3.Row
    return conn


@pytest.fixture(scope="module")
def pg_conn(load_env):
    dsl = {'dbname': load_env['pg_db'],
           'user': load_env['usr'],
           'password': load_env['pwd'],
           'host': load_env['host'],
           'port': load_env['port'],
           }
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


