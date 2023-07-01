import pytest
import os
import sqlite3

from dotenv import load_dotenv
from datetime import datetime
from contextlib import contextmanager, closing

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


@pytest.fixture(scope="module")
def lite_conn(load_env):
    sqlite3.register_converter(
        "timestamp",
        lambda x: datetime.fromisoformat(x.decode() + ':00')
    )
    conn = sqlite3.connect(load_env['lite_db_path'], detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def pg_conn(load_env):
    dsl = {'dbname': load_env['pg_db'],
           'user': load_env['usr'],
           'password': load_env['pwd'],
           'host': load_env['host'],
           'port': load_env['port'],
           }
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


