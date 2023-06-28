import pytest

from load_data import FilmworkModel, GenreModel, PersonModel, PersonFilmworkModel, GenreFilmworkModel


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
    lite_rows = lite_curs.fetchall()
    lite_data = [class_name(row) for row in lite_rows]

    with pg_conn.cursor() as pg_curs:
        pg_curs.execute(f'SELECT * FROM content.{table};')
        pg_rows = pg_curs.fetchall()
    pg_data = [class_name(row) for row in pg_rows]

    for lite, pg in zip(lite_data, pg_data):
        assert lite == pg, 'Не одинаковые'

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
        lite_count = lite_curs.fetchall()[0][0]

    with pg_conn as p_connect:
        pg_curs = p_connect.cursor()
        pg_curs.execute(f'SELECT COUNT(*) FROM content.{table};')
        pg_count = pg_curs.fetchone()[0]

    assert lite_count == pg_count





if __name__ == '__main__':
    pytest.main()
