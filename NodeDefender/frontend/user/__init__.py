from . import models, forms, views

UserView = Blueprint('UserView', __name__, template_folder="templates",
                      static_folder="../static")

