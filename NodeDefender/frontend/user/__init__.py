from flask import Blueprint
UserView = Blueprint('UserView', __name__, template_folder="templates",
                      static_folder="../static")
from . import models, forms, views
