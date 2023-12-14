import click
from flask import current_app
from flask.cli import with_appcontext
from domains.subdomain.models import Subdomain

from flaskshop.database import db

@click.command()
@with_appcontext
def create_starboy_subdomain():
    subdomain, _ = Subdomain.get_or_create(
        name='starboy.lvh.me'
    )
    click.echo(f"Subdomain {subdomain.name} created successfully.")

@click.command()
@with_appcontext
def create_emeraldlion_subdomain():
    subdomain, _ = Subdomain.get_or_create(
        name='emeraldlion.lvh.me'
    )
    click.echo(f"Subdomain {subdomain.name} created successfully.")
