# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import sys

from flask import Flask, abort, render_template, g, redirect, request, url_for


from flaskshop import commands
from flaskshop.extensions import (
    babel,
    bcrypt,
    bootstrap,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
)
from flaskshop.plugin import manager, spec
from flaskshop.plugin.models import PluginRegistry
from flaskshop.settings import Config
from flaskshop.subdomain.commands import create_emeraldlion_subdomain, create_starboy_subdomain
from flaskshop.subdomain.models import find_subdomain
from flaskshop.utils import jinja_global_varibles, log_slow_queries

def create_app(config_object=Config):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    app.pluggy = manager.FlaskshopPluginManager("flaskshop")
    register_extensions(app)
    load_plugins(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    jinja_global_varibles(app)
    log_slow_queries(app)
    return app


def register_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    app.before_request(lambda: before_request(app))
    babel.init_app(app)


def before_request(app):
    g.subdomain = find_subdomain(request.host.split(':')[0])
    if g.subdomain is None:
        abort(500)


def register_blueprints(app):
    app.pluggy.hook.flaskshop_load_blueprints(app=app)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"errors/{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.createdb)
    app.cli.add_command(commands.seed)
    app.cli.add_command(commands.flushrdb)
    app.cli.add_command(commands.reindex)
    app.cli.add_command(create_starboy_subdomain)
    app.cli.add_command(create_emeraldlion_subdomain)


def load_plugins(app):
    app.pluggy.add_hookspecs(spec)

    for name, module in sys.modules.items():
        if name.startswith("flaskshop"):
            app.pluggy.register(module)

    app.pluggy.load_setuptools_entrypoints("flaskshop_plugins")
    try:
        with app.app_context():
            for name in app.pluggy.external_plugins:
                plugin, _ = PluginRegistry.get_or_create(name=name)
                if not plugin.enabled:
                    app.pluggy.set_blocked(plugin.name)
    except Exception as e:
        # when db migrate raise exception
        app.logger.error(e)
