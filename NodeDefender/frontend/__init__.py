from .. import app
from admin import AdminView
from auth import AuthView
from data import DataView
from nodes import NodesView
from user import UserView

@app.context_processor
def inject_user():      # Adds general data to base-template
    if current_user.is_authenticated:
        # Return Message- inbox for user if authenticated
        messages = UserModel.query.get(current_user.id).messages
        return dict(user = current_user, messages = messages)
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
    return render_template('index.html', nodelist=nodes, stats = stats,
                           nodeevents = nodeevents)

# Register Blueprints
app.register_blueprint(AdminView)
app.register_blueprint(AuthView)
app.register_blueprint(DataView)
app.register_blueprint(NodesView)
app.register_blueprint(UserView)
