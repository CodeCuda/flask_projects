#
# Init module
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import Config


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
