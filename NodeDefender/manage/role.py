from .. import app, UserDatastore, db
from flask_script import Command, prompt, prompt_pass

class AddRole(Command):
    def run(self):
        email = prompt("User Email")
        user = UserDatastore.get_user(email)
        if not user:
            print("Unable to find user")
            return
        role = prompt("Role")
        UserDatastore.add_role_to_user(user, role)
        db.session.commit()
        print("Successfully added role {} to {}".format(role, email))

class CreateRole(Command):
    def run(self):
        name = prompt("Role name")
        description = prompt("Role Description")
        UserDatastore.create_role(name=name, description=description)
        db.session.commit()
        print("Successfully added role: {}".format(name))

class DeleteRole(Command):
    def run(self):
        pass

class ListRole(Command):
    def run(self):
        pass


