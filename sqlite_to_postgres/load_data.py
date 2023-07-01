import os
import uuid

import sqlite3
from contextlib import contextmanager, closing

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from datetime import datetime, date
from dotenv import load_dotenv

from dataclasses import dataclass, field, fields, astuple

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


@dataclass
class BasicModel:
    id: uuid.UUID
    created_at: datetime


@dataclass
class ModifiedModel:
    updated_at: datetime


@dataclass
class PersonModel(BasicModel, ModifiedModel):
    id: uuid.UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreModel(BasicModel, ModifiedModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class FilmworkModel(BasicModel, ModifiedModel):
    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    file_path: str
    type: str
    created_at: datetime
    updated_at: datetime
    rating: float = field(default=0.0)


@dataclass
class GenreFilmworkModel(BasicModel):
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@dataclass
class PersonFilmworkModel(BasicModel):
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def extract_movies(self, table, model, is_now=False):
        curs = self.conn.cursor()

        curs.execute(f'SELECT * FROM {table};')

        while records := curs.fetchmany(100):
            loaded_data = [model(**dict(record)) for record in records]
            yield loaded_data


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.conn = connection

    def save_all_data(self, table, model, rows):
        with self.conn.cursor() as curs:
            # получаем имена полей из модели
            column_names = ', '.join(field.name for field in fields(model))
            # %s под количество вставляемых значений
            template = ', '.join(['%s'] * len(fields(model)))
            for row in rows:
                res = curs.mogrify(f'({template})', astuple(row)).decode('utf-8')
                query = f"""
                    INSERT INTO content.{table} ({column_names}) VALUES {res} ON CONFLICT (id) DO NOTHING;
                """
                curs.execute(query)
            self.conn.commit()



def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)

    args = {
        'person': PersonModel,
        'genre': GenreModel,
        'film_work': FilmworkModel,
        'person_film_work': PersonFilmworkModel,
        'genre_film_work': GenreFilmworkModel,
    }

    for table, model in args.items():
        print(f'{table} -- {model}')
        data = sqlite_extractor.extract_movies(table, model, is_now=True)
        for rows in data:
            postgres_saver.save_all_data(table, model, rows)


@contextmanager
def conn_context(db_path: str):
    sqlite3.register_converter(
        "timestamp",
        lambda x: datetime.fromisoformat(x.decode() + ':00')
    )

    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


if __name__ == '__main__':
    lite_path = os.environ.get("DB_NAME_LITE")
    pg_db = os.environ.get("DB_NAME_PG")
    usr = os.environ.get("DB_USER")
    pwd = os.environ.get("DB_PASSWORD")
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT"))

    dsl = {'dbname': pg_db, 'user': usr, 'password': pwd, 'host': host, 'port': port}

    with conn_context(lite_path) as lite_conn, closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pgre_conn:
        load_from_sqlite(lite_conn, pgre_conn)

