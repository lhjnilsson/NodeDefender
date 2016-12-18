from flask import Blueprint
AdminView = Blueprint('AdminView', __name__, template_folder="templates",
                      static_folder="../static")

from . import models, forms, views
