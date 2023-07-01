import pytest

from load_data import FilmworkModel, GenreModel, PersonModel, PersonFilmworkModel, GenreFilmworkModel
from dataclasses import fields


@pytest.mark.parametrize(
    'table, class_name',
    (
        ('person', PersonModel),
        ('genre', GenreModel),
        ('film_work', FilmworkModel),
        ('person_film_work', PersonFilmworkModel),
        ('genre_film_work', GenreFilmworkModel),
    ),
)
def test_every_row(lite_conn, pg_conn, table, class_name):
    # with lite_conn as litesql_connection:
    lite_curs = lite_conn.cursor()
    lite_curs.execute(f'SELECT * FROM {table};')
    while lite_row := lite_curs.fetchone():
        lite_model = class_name(**lite_row)

        with pg_conn.cursor() as pg_curs:
            field_names = ', '.join([field.name for field in fields(class_name)])
            pg_curs.execute(f'SELECT {field_names} FROM content.{table} WHERE id=\'{lite_model.id}\';')
            pg_row = pg_curs.fetchone()
            postgre_model = class_name(**pg_row)
            assert lite_model == postgre_model


@pytest.mark.parametrize(
    'table',
    (
        'film_work',
        'person',
        'genre',
        'person_film_work',
        'genre_film_work',
    ),
)
def test_row_counts(lite_conn, pg_conn, table):
    with lite_conn as litesql_connection:
        lite_curs = litesql_connection.cursor()
        lite_curs.execute(f'SELECT COUNT(*) FROM {table};')
        lite_count = lite_curs.fetchone()[0]

    with pg_conn as p_connect:
        pg_curs = p_connect.cursor()
        pg_curs.execute(f'SELECT COUNT(*) FROM content.{table};')
        pg_count = pg_curs.fetchone()[0]
        print(pg_curs.fetchone())

    assert lite_count == pg_count


if __name__ == '__main__':
    pytest.main()
