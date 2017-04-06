from .. import app, LoginMan
from flask_login import login_required, current_user
from flask import Blueprint, render_template
from ..models.manage import node as NodeManage
from ..models.manage import data as DataManage
from itsdangerous import URLSafeSerializer
from ..models.SQL import UserModel

#Create Blueprint
AdminView = Blueprint('AdminView', __name__, template_folder="templates/admin",
                      static_folder="static")
AuthView = Blueprint('AuthView', __name__, template_folder="templates/auth",
                     static_folder="static")
DataView = Blueprint('DataView', __name__, template_folder="templates/data",
                      static_folder="static")
NodeView = Blueprint('NodeView', __name__, template_folder="templates/node",
                      static_folder="static")
UserView = Blueprint('UserView', __name__, template_folder="templates/user",
                      static_folder="static")

@LoginMan.user_loader
def load_user(id):
    return UserModel.query.get(id)

@app.context_processor
def inject_user():      # Adds general data to base-template
    if current_user:
        # Return Message- inbox for user if authenticated
        return dict(current_user = current_user)
    else:
        # If not authenticated user get Guest- ID(That cant be used).
        return dict(current_user = None)


@app.context_processor
def inject_serializer():
    def serialize(name):
        serializer = URLSafeSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(name)
    return dict(serialize = serialize)

@app.route('/')
@app.route('/index')
@login_required
def index():
    nodes = NodeManage.List(current_user.email)
    data = []
    events = [] 
    return render_template('dashboard/index.html', node=nodes, data = data, messages =
                          [], events = [])

from .admin import views
from .auth import views
from .data import views
from .nodes import views
from .user import views
from . import sockets

# Register Blueprints
app.register_blueprint(AdminView)
app.register_blueprint(AuthView)
app.register_blueprint(DataView)
app.register_blueprint(NodeView)
app.register_blueprint(UserView)
