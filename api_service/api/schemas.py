from api_service.extensions import ma


class UrlSchema(ma.Schema):
    short_url = ma.String(dump_only=True)
    long_url = ma.String(dump_only=True)
    count = ma.Integer(dump_only=True)
