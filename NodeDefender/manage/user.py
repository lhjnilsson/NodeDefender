from .. import app, UserDatastore, db
from flask_security import utils
from sys import exit
from flask_script import Command, prompt, prompt_pass
from ..models.SQL import UserModel


class CreateUserCommand(Command):
    def run(self):
        email = prompt("Email")
        if UserDatastore.get_user(email):
            print("Email already exists")
            print("Closing. Pleaser try again")
            return 
        pw1 = prompt_pass("Password")
        pw2 = prompt_pass("Password again");
        if pw1 != pw1:
            print("Passwords does not match!")
            print("Closing. Please try again")
            return
        encrypted_password = utils.encrypt_password(pw1)
        UserDatastore.create_user(email=email, password=encrypted_password)
        db.session.commit()

        print("Successfully added", email)

class DeleteUserCommand(Command):
    def run(self):
        email = prompt("Email")
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            print("Can't find user")
            return
        db.session.delete(user)
        db.session.commit()
        print("User Successfully deleted")

class ListUserCommand(Command):
    def run(self):
        for user in UserModel.query.all():
            print("ID: {}, Email: {}".format(user.id, user.email))
