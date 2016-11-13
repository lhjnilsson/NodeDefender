class GroupModel(db.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    

    def __init__(self):
        pass
