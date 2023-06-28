import os

import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from datetime import datetime
from typing import List
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


class BasicModel:
    def __init__(self, data, is_new=False):
        self.id = data[0]
        # Если требуется загрузить данные, включая время, то is_new=False
        if not is_new:
            self.created = data[1]
            self.modified = data[2]
            if isinstance(data[1], str):
                # Время в SQLite хранится в строке в формате UTC со смещением +00.
                # Нужно сконвертировать в подходящий для парсера вариант
                convert_date = data[1].replace('+00', '+00:00')
                self.created = datetime.strptime(convert_date, '%Y-%m-%d %H:%M:%S.%f%z')
            if isinstance(data[2], str):
                convert_date = data[2].replace('+00', '+00:00')
                self.modified = datetime.strptime(convert_date, '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            now = datetime.utcnow()
            self.created = now
            self.modified = now


class PersonModel(BasicModel):
    def __init__(self, data, is_new=False):
        super().__init__((data[0],
                          data[2],
                          data[3],
                          ),
                         is_new
                         )
        self.full_name = data[1]

    def __str__(self):
        res = 'Запись №: {0}\nИмя: {1} \nЗапись создана: {2}\nЗапись изменена: {3}'.format(
            self.id,
            self.full_name,
            self.created,
            self.modified,
        )
        return res

    def __eq__(self, other):
        # сравнение двух людей
        if isinstance(other, PersonModel):
            return (self.id == other.id and
                    self.full_name == other.full_name and
                    self.created == other.created and
                    self.modified == other.modified)
        # иначе возвращаем NotImplemented
        return NotImplemented


class GenreModel(BasicModel):
    def __init__(self, data, is_new=False):
        super().__init__((data[0],
                          data[3],
                          data[4],
                          ),
                         is_new
                         )
        self.name = data[1]
        self.description = data[2]

    def __str__(self):
        res = 'Запись №: {0}\nИмя: {1} \nЗапись создана: {2}\nЗапись изменена: {3}'.format(
            self.id,
            self.name,
            self.created,
            self.modified,
        )
        return res

    def __eq__(self, other):
        # сравнение двух жанров
        if isinstance(other, GenreModel):
            return (self.id == other.id and
                    self.name == other.name and
                    self.created == other.created and
                    self.modified == other.modified)
        # иначе возвращаем NotImplemented
        return NotImplemented


class FilmworkModel(BasicModel):
    def __init__(self, data, is_new=False):
        super().__init__(
                         (data[0],
                          data[6],
                          data[7],
                          ),
                         is_new
                         )
        self.title = data[1]
        self.description = data[2]
        self.creation_date = data[3]
        self.rating = data[4]
        self.type = data[5]

    def __str__(self):
        res = """Запись №: {0}\nИмя картины: {1} \nДата создания: {2} и рейтинг {3}\
        \nТип: {4}\nЗапись создана: {5}\nЗапись изменена: {6}""".format(
            self.id,
            self.title,
            self.creation_date,
            self.rating,
            self.type,
            self.created,
            self.modified,
        )
        return res

    def __repr__(self):
        res = """Запись №: {0}\nИмя картины: {1} \nДата создания: {2} и рейтинг {3}\
        \nТип: {4}\nЗапись создана: {5}\nЗапись изменена: {6}""".format(
            self.id,
            self.title,
            self.creation_date,
            self.rating,
            self.type,
            self.created,
            self.modified,
        )
        return res


    def __eq__(self, other):
        # сравнение двух фильмов
        if isinstance(other, FilmworkModel):
            return (self.id == other.id and
                    self.title == other.title and
                    self.creation_date == other.creation_date and
                    self.rating == other.rating and
                    self.type == other.type and
                    self.created == other.created and
                    self.modified == other.modified)
        # иначе возвращаем NotImplemented
        return NotImplemented


class GenreFilmworkModel:
    def __init__(self, data, is_new=False):
        self.id = data[0]
        self.film_work_id = data[1]
        self.genre_id = data[2]
        # Если требуется скопировать время, то is_new=False
        if not is_new:
            self.created = data[3]
            if isinstance(data[3], str):
                # Время в SQLite хранится в строке в формате UTC со смещением +00.
                # Нужно сконвертировать в подходящий для парсера вариант
                convert_date = data[3].replace('+00', '+00:00')
                self.created = datetime.strptime(convert_date, '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            now = datetime.utcnow()
            self.created = now

    def __eq__(self, other):
        # сравнение двух таблиц
        if isinstance(other, GenreFilmworkModel):
            return (self.id == other.id and
                    self.film_work_id == other.film_work_id and
                    self.genre_id == other.genre_id and
                    self.created == other.created)
        # иначе возвращаем NotImplemented
        return NotImplemented


class PersonFilmworkModel:
    def __init__(self, data, is_new=False):
        self.id = data[0]
        self.film_work_id = data[1]
        self.person_id = data[2]
        self.role = data[3]
        # Если требуется скопировать время, то is_new=False
        if not is_new:
            self.created = data[4]
        else:
            now = datetime.utcnow()
            self.created = now

    def __eq__(self, other):
        # сравнение двух таблиц
        if isinstance(other, PersonFilmworkModel):
            return (self.id == other.id and
                    self.film_work_id == other.film_work_id and
                    self.person_id == other.person_id and
                    self.role == other.role and
                    self.created == other.created)
        # иначе возвращаем NotImplemented
        return NotImplemented


class StructToExtract:
    def __init__(self,
                 persons_to_load,
                 genres_to_load,
                 films_to_load,
                 person_films_to_load,
                 genre_films_to_load):
        self.persons: List[PersonModel] = persons_to_load
        self.genres: List[GenreModel] = genres_to_load
        self.films: List[FilmworkModel] = films_to_load
        self.persons_films: List[PersonFilmworkModel] = person_films_to_load
        self.genres_films: List[GenreFilmworkModel] = genre_films_to_load


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def extract_movies(self, is_now=False):
        curs = self.conn.cursor()

        # Последовательность считываемых таблиц и данных не важна.
        # Важность последовательности наступает при вствке в другую БД (из-за внешних ключей)
        curs.execute("SELECT * FROM person;")
        records = curs.fetchall()
        persons_to_load = [PersonModel(record) for record in records]

        curs.execute("SELECT * FROM genre;")
        records = curs.fetchall()
        genres_to_load = [GenreModel(record) for record in records]

        curs.execute('PRAGMA table_info(film_work);')
        records = curs.fetchall()
        if 'file_path' in records[1]:
            curs.execute('ALTER TABLE film_work DROP COLUMN file_path;')

        curs.execute('SELECT * FROM film_work;')
        records = curs.fetchall()
        films_to_load = [FilmworkModel(record) for record in records]

        curs.execute("SELECT * FROM person_film_work;")
        records = curs.fetchall()
        person_films_to_load = [PersonFilmworkModel(record) for record in records]

        curs.execute("SELECT * FROM genre_film_work;")
        records = curs.fetchall()
        genre_films_to_load = [GenreFilmworkModel(record) for record in records]

        """ debug
        for i, itm in enumerate(films_to_load, start=1):
            print('{0}: {1}'.format(i, itm))
        print('end')
        """

        return StructToExtract(persons_to_load,
                               genres_to_load,
                               films_to_load,
                               person_films_to_load,
                               genre_films_to_load)


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.conn = connection

    def save_all_data(self, data: StructToExtract, truncate_on_start=False):
        with self.conn.cursor() as curs:
            if truncate_on_start:
                # Очищаем таблицы, если надо грузиться в пустую БД
                curs.execute("""TRUNCATE content.person_film_work""")
                curs.execute("""TRUNCATE content.genre_film_work""")
                curs.execute("""TRUNCATE content.film_work CASCADE""")
                curs.execute("""TRUNCATE content.person CASCADE""")
                curs.execute("""TRUNCATE content.genre CASCADE""")

            # Множественный INSERT
            # Жанры
            all_data = [(record.id,
                         record.name,
                         record.description,
                         record.created,
                         record.modified) for record in data.genres]
            args = ','.join(curs.mogrify("(%s, %s, %s, %s, %s)", item).decode() for item in all_data)
            curs.execute(f"""
            INSERT INTO content.genre (id, name, description, created, modified)
            VALUES {args}
            """)

            # Персоналии
            all_data = [(record.id,
                         record.full_name,
                         record.created,
                         record.modified) for record in data.persons]
            args = ','.join(curs.mogrify("(%s, %s, %s, %s)", item).decode() for item in all_data)
            curs.execute(f"""
            INSERT INTO content.person (id, full_name, created, modified)
            VALUES {args}
            """)

            # Фильмы
            all_data = [(record.id,
                         record.title,
                         record.description,
                         record.creation_date,
                         record.rating,
                         record.type,
                         record.created,
                         record.modified) for record in data.films]
            args = ','.join(curs.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", item).decode() for item in all_data)
            curs.execute(f"""
            INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created, modified)
            VALUES {args}
            """)

            # Фильмы-персоны (ManyToMany)
            all_data = [(record.id,
                         record.film_work_id,
                         record.person_id,
                         record.role,
                         record.created) for record in data.persons_films]
            args = ','.join(curs.mogrify("(%s, %s, %s, %s, %s)", item).decode() for item in all_data)
            curs.execute(f"""
            INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created)
            VALUES {args}
            """)

            # Фильмы-жанры (ManyToMany)
            all_data = [(record.id,
                         record.film_work_id,
                         record.genre_id,
                         record.created) for record in data.genres_films]
            args = ','.join(curs.mogrify("(%s, %s, %s, %s)", item).decode() for item in all_data)
            curs.execute(f"""
            INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created)
            VALUES {args}
            """)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    # sqlite_extractor = SQLiteExtractor(connection)
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)

    # data = sqlite_extractor.extract_movies()
    # postgres_saver.save_all_data(data)
    data = sqlite_extractor.extract_movies(is_now=True)
    postgres_saver.save_all_data(data, truncate_on_start=True)


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


if __name__ == '__main__':
    lite_db_path = os.environ.get("DB_NAME_LITE")
    pg_db = os.environ.get("DB_NAME_PG")
    usr = os.environ.get("DB_USER")
    pwd = os.environ.get("DB_PASSWORD")
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT"))

    dsl = {'dbname': pg_db, 'user': usr, 'password': pwd, 'host': host, 'port': port}

    with conn_context(lite_db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
