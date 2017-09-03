from flask import Blueprint, render_template
from NodeDefender import app
from flask_login import login_required

admin_view = Blueprint('admin_view', __name__, template_folder="templates/admin",
                      static_folder="static")
auth_view = Blueprint('auth_view', __name__, template_folder="templates/auth",
                     static_folder="static")
data_view = Blueprint('data_view', __name__, template_folder="templates/data",
                      static_folder="static")
node_view = Blueprint('node_view', __name__, template_folder="templates/node",
                      static_folder="static")
user_view = Blueprint('user_view', __name__, template_folder="templates/user",
                      static_folder="static")

# Register Blueprints
app.register_blueprint(admin_view)
app.register_blueprint(auth_view)
app.register_blueprint(data_view)
app.register_blueprint(node_view)
app.register_blueprint(user_view)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('frontend/dashboard/index.html')


import NodeDefender.frontend.views.admin
import NodeDefender.frontend.views.auth
import NodeDefender.frontend.views.data
import NodeDefender.frontend.views.nodes
import NodeDefender.frontend.views.user
