from . import models, forms, views

AuthView = Blueprint('AuthView', __name__, template_folder="templates",
                      static_folder="../static")

