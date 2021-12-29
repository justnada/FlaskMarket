from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# config app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "1a2e4a56d6595f380fff95b3"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# redirect to login when unauthorized user try to access market_page
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
