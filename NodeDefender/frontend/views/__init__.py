from flask import Blueprint, render_template

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

# Register Blueprints
app.register_blueprint(AdminView)
app.register_blueprint(AuthView)
app.register_blueprint(DataView)
app.register_blueprint(NodeView)
app.register_blueprint(UserView)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('dashboard/index.html')


import NodeDefender.frontend.views.admin
import NodeDefender.frontend.views.auth
import NodeDefender.frontend.views.data
import NodeDefender.frontend.views.nodes
import NodeDefender.frontend.views.user
