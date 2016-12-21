from .. import UserDatastore, db
from flask_script import Command, prompt, prompt_pass
from ..models.SQL import UserModel, GroupModel

class CreateGroupCommand(Command):
    def run(self):
        groupname = prompt('Group name')
        exists = GroupModel.query.filter_by(name=groupname).first()
        if exists:
            print("Group {} is already present.".format(groupname))
            return
        group = GroupModel(groupname)
        db.session.add(group)
        db.session.commit()
        print("Group {} Successfully added!".format(groupname))
        return

class AddUserCommand(Command):
    def run(self):
        groupname = prompt('Group name')
        group = GroupModel.query.filter_by(name=groupname).first()
        if group is None:
            print("Unable to find Group {}".format(groupname))
            return

        email = prompt('User email')
        user = UserModel.query.filter_by(email=email).first()
        if user is None:
            print("Unable to find user {}".format(username))
            return

        group.users.append(user)
        db.session.add(group)
        db.session.commit()
        print("Successfully added {} to {}".format(email, groupname))
        return

class ListGroupCommand(Command):
    def run(self):
        for group in GroupModel.query.all():
            print("ID: {}, Name: {}".format(group.id, group.name))
        return

class ListMemberCommand(Command):
    def run(self):
        groupname = prompt("Group name")
        group = GroupModel.query.filter_by(name = groupname).first()
        for member in group.users:
            print(member.email)

        return


