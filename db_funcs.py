'''20/01/2018 functions for settiing up, adding to and getting scores from a db'''

import psycopg2 as pg2

def conn_open_close(func):
    def wrapper(*args):
        global conn #need to be global so wrapped function can use them
        global cur
        conn = pg2.connect(database='snake', user='postgres', password='postgres123')
        cur = conn.cursor()
        return_var = func(*args)
        conn.commit() #get_score() doesn't need this line but easier to leave in and doesn't cause an error
        conn.close()
        return return_var
    return wrapper


@conn_open_close
def setup_DB(dbtable):
    cur.execute(f'CREATE TABLE IF NOT EXISTS {dbtable}('
                + 'id serial PRIMARY KEY, '
                + "f_name VARCHAR(50) NOT NULL DEFAULT 'unknown', "
                + "l_name VARCHAR(50) NOT NULL DEFAULT 'unknown', "
                + 'score integer NOT NULL, '
                + 'date_played timestamp not null DEFAULT CURRENT_TIMESTAMP)')


@conn_open_close
def add_score(dbtable, f_name, l_name, score):
    #f-string is for adding variables into the string
    cur.execute(f"INSERT INTO {dbtable} (f_name, l_name, score) VALUES ('{f_name}', '{l_name}', {score})")


@conn_open_close
def get_scores(dbtable):
    cur.execute(f'SELECT f_name, l_name, score FROM {dbtable} ORDER BY score DESC LIMIT 100')
    return cur.fetchall()
