from flask import render_template
# , flash, redirect, url_for, request
# from werkzeug.urls import url_parse
# from app import db
# from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_required

# current_user, login_user, logout_user
# from app.models import User
# from app.auth import bp


# ...
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')
