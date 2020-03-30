import pymysql
from pymysql.constants import CLIENT
from flask import current_app,g,abort
import click
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db=pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            port=current_app.config['DB_PORT'],
            charset=current_app.config['DB_CHARSET'],
            database=current_app.config['DATABASE']
            )
    g.db.ping(reconnect=True)
    return g.db

def get_db_with_multi_statements():
    if 'db_with_multi_statements' not in g:
        g.db_with_multi_statements=pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            port=current_app.config['DB_PORT'],
            charset=current_app.config['DB_CHARSET'],
            database=current_app.config['DATABASE'],
            client_flag = CLIENT.MULTI_STATEMENTS
        )
    g.db_with_multi_statements.ping(reconnect=True)
    return g.db_with_multi_statements

def get_db_with_dict_cursor():
    if 'db_with_dict_cursor' not in g:
        g.db_with_dict_cursor=pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            port=current_app.config['DB_PORT'],
            charset=current_app.config['DB_CHARSET'],
            database=current_app.config['DATABASE'],
            client_flag = CLIENT.MULTI_STATEMENTS,
            cursorclass=pymysql.cursors.DictCursor
        )
    g.db_with_dict_cursor.ping(reconnect=True)
    return g.db_with_dict_cursor


def close_db(e=None):
    for db_name in ['db','db_with_dict_cursor','db_with_multi_statements']:
        db=g.pop(db_name,None)
        if db is not None and db.open:
            db.close()

def init_db():
    db=get_db_with_multi_statements()
    for table_name in current_app.config['DB_TABLES']:
        with current_app.open_resource('../db_source/%s.sql' % table_name) as f:
            print("opening %s..." % table_name)
            cursor=db.cursor()
            sql=f.read().decode('utf8')
            cursor.execute(sql)
    db.commit()
    db.close()

def db_required(func):
    def wrapper(*args, **kwargs):
        db=get_db()
        func(*args,**kwargs)
        db.close()
    return wrapper



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)