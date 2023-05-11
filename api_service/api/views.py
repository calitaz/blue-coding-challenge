from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from api_service.api import resources

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(resources.UrlShortner, "/url", endpoint="url")
api.add_resource(
    resources.RedirectURL, "/redirect/<string:short_code>", endpoint="redirect"
)
api.add_resource(resources.UrlStats, "/stats", endpoint="stats")


@blueprint.errorhandler(ValidationError)
def handle_schemas_errors(e):
    return jsonify(e.messages), 422
