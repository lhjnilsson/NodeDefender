import NodeDefender
from flask import Blueprint, make_response, jsonify

api_view = Blueprint("api_view", __name__)

def load_api(app):
    global api
    NodeDefender.app.register_blueprint(api_view, url_prefix="/api/v1")
    return True

import NodeDefender.frontend.api.config
