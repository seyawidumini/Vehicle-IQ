from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user
import pickle,os,json

app = Flask(__name__)
app.config['SECRET_KEY']='46ced26eca7241daacbd4280470e9612'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///vehicle.db"
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = "info"

from main.models import Admin, User

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    return User.query.get(int(user_id))

with open("main/artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("main/artifacts/model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

from main import routes