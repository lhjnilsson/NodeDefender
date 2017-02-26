def CleanDuplicate(records):
    for icpe, node in records:
        if node.parent_id == None:
            db.session.delete(node)
    db.session.commit()
    return True

from . import sockets
