import os

# Configure file for app
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Class for app configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    UPLOAD_FOLDER = 'app/static/images/'
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
