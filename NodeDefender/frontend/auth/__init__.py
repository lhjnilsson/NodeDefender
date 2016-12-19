from flask import Blueprint

AuthView = Blueprint('AuthView', __name__, template_folder="templates",
                      static_folder="../static")
from . import models, forms, views


