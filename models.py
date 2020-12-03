from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    user = db.relationship('Feedback', backref='users')

    @classmethod
    def register(cls, user_name, pwd, email, f_name, l_name):
        """Register user w/ hashed pw"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=user_name, password=hashed_utf8, email=email, first_name=f_name, last_name=l_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user exists & password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.String(100), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    feedback_about = db.Column(db.Text)
    feedback_from = db.Column(db.Text, db.ForeignKey('users.username'))


    

    