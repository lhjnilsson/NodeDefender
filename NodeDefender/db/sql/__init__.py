import NodeDefender
from flask_sqlalchemy import SQLAlchemy

SQL = SQLAlchemy()

def load(app):
    global SQL
    print("Here")
    SQL.app = app
    with app.app_context():
        SQL.init_app(app)
        SQL.create_all()
    print("he")
    if NodeDefender.config.general.run_mode == 'TESTING':
        print("creating")
        SQL.create_all()
    return True

from NodeDefender.db.sql.group import GroupModel
from NodeDefender.db.sql.user import UserModel
from NodeDefender.db.sql.node import NodeModel, LocationModel
from NodeDefender.db.sql.icpe import iCPEModel, SensorModel,\
        CommandClassModel, CommandClassTypeModel
from NodeDefender.db.sql.data import PowerModel, HeatModel, EventModel
from NodeDefender.db.sql.conn import MQTTModel
from NodeDefender.db.sql.message import MessageModel


