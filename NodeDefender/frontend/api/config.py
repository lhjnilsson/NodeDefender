import json
from flask_restful import Resource, reqparse
import NodeDefender

parser = reqparse.RequestParser()
parser.add_argument("config")

def load_api(api):
    api.add_resource(GeneralConfig, '/api/v1/config/general')
    print("loaded")
    return True

class General(Resource):
    def get(self):
        config = NodeDefender.config.general.config
        return config
    def put(self):
        args = parser.parse_args()
        print(args)
        json.loads(args['config'].replace("'", "\""))
        try:
            config = json.loads(args['config'])
        except (KeyError, ValueError):
            return args, 400
        print(config)
        config = NodeDefender.config.general.set_config(**config)
        return args, 202

class GeneralConfig(Resource):
    def get(self, key):
        try:
            return NodeDefender.config.general.config[key]
        except KeyError:
            return None

    def put(self, key):
        pass



