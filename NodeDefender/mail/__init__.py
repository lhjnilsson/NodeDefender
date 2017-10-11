from flask_mail import Mail
import logging
import NodeDefender

mail = Mail(NodeDefender.app)

logger = logging.getLogger("mail")
logger.setLevel("INFO")
logger.addHandler(NodeDefender.loggHandler)

import NodeDefender.mail.user
import NodeDefender.mail.group
import NodeDefender.mail.node
import NodeDefender.mail.icpe
