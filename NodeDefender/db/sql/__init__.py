from flask_sqlalchemy import SQLAlchemy
SQL = SQLAlchemy()

def load(app):
    global SQL
    SQL.init_app(app)
    if NodeDefender.config.general.run_mode == 'TESTING':
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


