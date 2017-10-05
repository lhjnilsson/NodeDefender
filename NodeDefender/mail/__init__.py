from NodeDefender import app
from flask_mail import Mail

mail = Mail(app)

import NodeDefender.mail.user
import NodeDefender.mail.group
import NodeDefender.mail.node
import NodeDefender.mail.icpe
