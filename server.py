"""Backend routes and Flask config."""
import os
from flask import Flask
from flask import flash, jsonify, redirect, render_template, request
from flask_login import LoginManager
from flask_login import current_user, login_required, login_user, logout_user
from google_api import *
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
    """Redirects users to home or registration page based on user state."""
    if not current_user.is_authenticated:
        return redirect('/register')
    return redirect('/home')


@app.route('/register')
@app.route('/login')
def logged_out():
    """Passes view routing to client. Takes authenticated users home."""
    if current_user.is_authenticated:
        flash('Already logged in.', 'info')
        return redirect('/home')
    return render_template('logged_out.html')


@app.route('/home')
@app.route('/new-habit')
@app.route('/account')
@app.route('/habit')
@login_required
def logged_in():
    """Passes view routing to client."""
    return render_template('logged_in.html')


@app.route('/logout')
def logout():
    """Logs user out if user was logged in. Redirects to login."""
    if current_user.is_authenticated:
        logout_user()
        flash('See you next time!', 'success')
    return redirect('/login')


# -------------------- authentication --------------------

@app.route('/auth/process-registration', methods=['POST'])
def process_registration():
    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        flash('An account with that email address already exists.', 'error')
        return redirect('/login')

    password = hash_password(request.form.get('password'))
    location = request.form.get('location')
    timezone = request.form.get('timezone')

    user = User(email=email, password=password, location=location,
                timezone=timezone)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash('Welcome!', 'success')
    return redirect('/home')


@app.route('/auth/validate-login', methods=['POST'])
def validate_login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('No user with that email address found.', 'error')
        return redirect('/login')
    elif not user.verify_password(password):
        flash('Incorrect password.', 'error')
        return redirect('/login')

    login_user(user, remember=remember)
    flash('Welcome back!', 'success')
    return redirect('/home')


# -------------------- json --------------------

@app.route('/json/validate-location', methods=['GET'])
def validate_location():
    """Validates given location and bundles JSON name / timezone data."""
    location = request.args.get('location')

    try:
        possible_locations = bundle_location_data(location)
    except NoLocationResultsError as e:
        return jsonify({'error': e.message})

    return jsonify(possible_locations)


@app.route('/json/get-current-user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(current_user.dictionarify())


@app.route('/json/get-user-habits', methods=['GET'])
@login_required
def get_user_habits():
    res = [h.dictionarify() for h in current_user.habits]
    return jsonify(res)


@app.route('/json/get-habit', methods=['GET'])
@login_required
def get_habit():
    habit_id = request.args.get('habit-id')
    habit = Habit.query.get(habit_id)

    if not habit:
        return jsonify({'error': 'Habit not found.'})
    elif habit.user_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized.'})

    completions = [c.dictionarify() for c in habit.completions]
    return jsonify({'habit': habit.dictionarify(), 'completions': completions})


# -------------------- api --------------------

@app.route('/api/add-habit', methods=['POST'])
@login_required
def add_habit():
    title = request.form.get('title')
    user_id = current_user.user_id
    # optional fields
    min_goal = None
    max_goal = None

    if bool(request.form.get('min-freq')):
        min_goal = request.form.get('min-goal')

    if bool(request.form.get('max-freq')):
        max_goal = request.form.get('max-goal')

    # can be None, this is fine
    timeframe = request.form.get('timeframe')

    habit = Habit(user_id=user_id, title=title, min_goal=min_goal,
                  max_goal=max_goal, timeframe=timeframe)
    db.session.add(habit)
    db.session.commit()
    flash('Good luck!', 'success')
    return redirect('/home')


@app.route('/api/complete-habit', methods=['POST'])
@login_required
def complete_habit():
    habit_id = request.form.get('habit-id')
    habit = Habit.query.get(habit_id)
    if habit.user_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized.'})
    completion = Completion(habit_id=habit_id)
    db.session.add(completion)
    db.session.commit()
    flash('Successfully logged completion.', 'success')
    return redirect('/home')


@app.route('/api/delete-habit')
@login_required
def delete_habit():
    habit_id = request.args.get('habit-id')
    habit = Habit.query.get(habit_id)

    if habit.user_id != current_user.user_id:
        return jsonify('error')

    for completion in habit.completions:
        db.session.delete(completion)

    db.session.delete(habit)
    db.session.commit()
    return jsonify('success')


@app.route('/api/update-name', methods=['POST'])
@login_required
def update_name():
    current_user.name = request.json['name']
    db.session.commit()
    return jsonify('success')


@app.route('/api/update-sms', methods=['POST'])
@login_required
def update_sms():
    pass


# -------------------- server --------------------

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
