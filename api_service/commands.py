import requests
from bs4 import BeautifulSoup
import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""
    pass


@cli.command("clear-db")
@with_appcontext
def clear_db():
    from api_service.extensions import db

    db.drop_all()


@cli.command("init-db")
@with_appcontext
def init_db():
    from api_service.extensions import db

    db.create_all()


@cli.command("crawler")
@with_appcontext
def crawler():
    click.echo("Starting bot")
    from api_service.extensions import db
    from api_service.models import Url, BotUrl

    urls = Url.query.all()

    for url in urls:
        # send HTTP GET request to the URL and retrieve the HTML content
        response = requests.get(url.long_url)
        html = response.text

        # parse the HTML using BeautifulSoup and extract the title tag
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string
        click.echo(f"Title found: {title}")

        bot_data = BotUrl(title=title if title else "Not Found", url_id=url.id)
        db.session.add(bot_data)
        db.session.commit()

    click.echo("Bot finished")
