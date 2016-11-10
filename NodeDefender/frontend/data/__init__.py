from . import models, forms, views

DataView = Blueprint('DataView', __name__, template_folder="templates",
                      static_folder="../static")

