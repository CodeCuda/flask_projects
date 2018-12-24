#
# This module contains db classes
#
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.face_detect import detect_face, verify_faces


class User(UserMixin, db.Model):
    """
    User class
    Contains info for db and functionality to validate login
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    photo_id = db.Column(db.String(128))


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        Set User's Password
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check User's password
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def check_photo(self, id):
        """
        Check User's photo from db
        :param img_url:
        :return:
        """

        user_face_id = detect_face(self.photo_id)

        result = verify_faces(id, user_face_id)
        return result


@login.user_loader
def load_user(id):
    """
    Load User
    :param id:
    :return:
    """
    return User.query.get(int(id))
