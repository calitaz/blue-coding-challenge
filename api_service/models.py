from api_service.extensions import db


class Url(db.Model):
    """Db model for the Url shortner"""

    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(255), unique=True)
    long_url = db.Column(db.String(255), nullable=False, unique=True)
    short_code = db.Column(db.String(255), unique=True)
    count = db.Column(db.Integer, default=0)


class BotUrl(db.Model):
    """Db model for the bot"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default="Not Found")
    url_id = db.Column(db.Integer, db.ForeignKey("url.id"), nullable=False)
    url = db.relationship("Url", backref="url")
