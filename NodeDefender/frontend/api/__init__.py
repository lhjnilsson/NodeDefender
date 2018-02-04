import NodeDefender
import NodeDefender.frontend.api.config
from flask_restful import Api

api = None

def load_api(app):
    global api
    api = Api(app)
    print("loading")
    NodeDefender.frontend.api.config.load_api(api)
    return True
