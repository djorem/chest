"""Database module, including the pickledb database object and utilities."""

import pickledb

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Returns a pickledb object from the contents of g"""
    if 'db' not in g:
        g.db = pickledb.load(current_app.config['DATABASE'], True, sig=False)
    return g.db


def init_db():
    """Clear the existing data and create new tables."""
    database = get_db()
    database.deldb()
    database.dump()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register init_db_command in the app"""
    app.cli.add_command(init_db_command)
