from .. import app
from flask_login import login_required, current_user
from flask import Blueprint
from . import assets

#Create Blueprint
AdminView = Blueprint('AdminView', __name__, template_folder="templates/admin",
                      static_folder="static")
DataView = Blueprint('DataView', __name__, template_folder="templates/data",
                      static_folder="static")
NodeView = Blueprint('NodeView', __name__, template_folder="templates/node",
                      static_folder="static")
UserView = Blueprint('UserView', __name__, template_folder="templates/user",
                      static_folder="static")

assets.init(app)

@app.context_processor
def inject_user():      # Adds general data to base-template
    if current_user.is_authenticated:
        # Return Message- inbox for user if authenticated
        return dict(user = current_user)
    else:
        # If not authenticated user get Guest- ID(That cant be used).
        return dict(user = current_user)

@app.route('/')
@app.route('/index')
@login_required
def index():
    nodes = iCPEModel.query.all()
    stats = statistics.GetAllStats()
    nodeevents = NodeEventModel.query.order_by(desc(NodeEventModel.id)).limit(20)
    return render_template('index.html', nodelist=nodes, stats = stats, nodeevents = nodeevents)

from .admin import views
from .data import views
from .nodes import views
from .user import views

# Register Blueprints
app.register_blueprint(AdminView)
app.register_blueprint(DataView)
app.register_blueprint(NodeView)
app.register_blueprint(UserView)
