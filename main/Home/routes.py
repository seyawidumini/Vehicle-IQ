from flask import Blueprint,render_template
from main import app

index=Blueprint('index',__name__)

@index.route('/')
def home():
    return render_template('user/index.html')