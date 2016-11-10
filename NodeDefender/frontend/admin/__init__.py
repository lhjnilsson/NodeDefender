from . import models, forms, views

AdminView = Blueprint('AdminView', __name__, template_folder="templates",
                      static_folder="../static")

