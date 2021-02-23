# models.py
from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# We need to add loaduser function here, this is basically going to allow flask login to 
# load the current user and grab their login ID. So we can show them pages specific to their 
# login ID.

# builtin decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Usermixin has all those management features of login and authorization thats why we inherit frm it
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__ (self, email, username, mypassword):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(mypassword)

    def check_password(self, mypassword):
        return check_password_hash(self.password_hash, mypassword)
