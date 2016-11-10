from . import models, forms, views

def CleanDuplicate(records):
    for icpe, node in records:
        if node.parent_id == None:
            db.session.delete(node)
    db.session.commit()
    return True

NodeView = Blueprint('NodeView', __name__, template_folder="templates",
                      static_folder="../static")

