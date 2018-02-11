import NodeDefender
from flask import Blueprint, make_response, jsonify

api_view = Blueprint("api_view", __name__)

@api_view.route("/test", methods=["GET"])
def test_api():
    return jsonify({'IT IS' : 'WORKING'}), 200
    #return make_response(jsonify({'status' : "OK",
    #                              'message' : "Hello this works!"})), 200

def load_api(app):
    global api
    NodeDefender.app.register_blueprint(api_view, url_prefix="/api/v1")
    return True

import NodeDefender.frontend.api.config
