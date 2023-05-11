from flask import Flask
from api_service import api
from api_service.extensions import db
from api_service.extensions import migrate
from .commands import init_db, clear_db, crawler


def create_app(testing=False):
    app = Flask("api_service")
    app.config.from_object("api_service.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)

    app.cli.add_command(init_db)
    app.cli.add_command(clear_db)
    app.cli.add_command(crawler)

    register_blueprints(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


if __name__ == "__main__":
    app = create_app()
