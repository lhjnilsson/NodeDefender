from .. import app
from flask_mail import Mail

mail = Mail(app)

from . import user, group, icpe
