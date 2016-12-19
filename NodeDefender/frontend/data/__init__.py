from flask import Blueprint
DataView = Blueprint('DataView', __name__, template_folder="templates",
                      static_folder="../static")
from . import models, forms, views
