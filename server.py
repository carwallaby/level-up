"""Backend routes and Flask config."""
import arrow
import os
from flask import Flask
from flask import flash, jsonify, redirect, render_template, request
from flask_login import LoginManager
from flask_login import current_user, login_required, login_user, logout_user
from models import *

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.environ['SUPER_SECRET']

login_manager = LoginManager()
login_manager.init_app(app)


# -------------------- login manager --------------------

@login_manager.user_loader
def load_user(user_id):
    """Gets user by unicode user ID."""
    return User.query.get(ord(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Handles logged-out users accessing login required pages."""
    flash('You must be logged in to view that page.', 'error')
    return redirect('/login')


# -------------------- pages --------------------

@app.route('/')
def index():
    return 'hello'


# -------------------- server --------------------

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
