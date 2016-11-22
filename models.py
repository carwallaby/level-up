"""Database models and helper functions."""
import arrow
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
# initializes database
db = SQLAlchemy()


# -------------------- models --------------------

class User(db.Model):
    """A user."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    timezone = db.Column(db.String(100), nullable=False)
    signed_up = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # ---------- optional fields ----------
    name = db.Column(db.String(100), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    sms_num = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    reminders = db.Column(db.Enum('daily', 'weekly', name='reminder'),
                          nullable=True)
    # ---------- success metrics ----------
    last_week_success = db.Column(db.Float, nullable=True)
    total_success = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """Representation of a user."""
        return '<User {} {}>'.format(self.user_id, self.username)

    # ---------- password verification ----------

    def verify_password(self, password):
        """Verifies given password against stored SHA256 hash."""
        return pbkdf2_sha256.verify(password, self.password)

    # ---------- dates / times ----------

    def current_arrow(self):
        """Gets user's local date/time as an Arrow object."""
        return arrow.now(self.timezone)

    def convert_utc_to_local(self, utc_datetime):
        """Converts UTC datetime into Arrow in user's timezone."""
        return arrow.get(utc_datetime).to(self.timezone)

    def is_birthday(self):
        """Returns whether today's date is user's birthday."""
        if not self.birthdate:
            # user hasn't set their birthdate
            return False
        today = self.current_arrow().date()
        return today == self.birthdate.replace(year=today.year)

    def _is_midnight(self):
        """Returns whether it is midnight (0:00 - 0:59) in user's timezone.
        Used for success calculations."""
        return self.current_arrow().hour == 0

    def _is_sunday(self):
        """Returns whether it is Sunday in user's timezone.
        Used for success calculations."""
        return self.current_arrow().weekday() == 6

    # ---------- success ----------

    def get_success_counted_habits(self):
        """Gets user's habits that count for success metrics."""
        return [h for h in self.habits if h.timeframe]

    # ---------- login manager ----------

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """Returns user ID as unicode."""
        return unichr(self.user_id)


class Habit(db.Model):
    """A habit."""
    __tablename__ = 'habits'

    habit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # ---------- optional fields ----------
    min_goal = db.Column(db.Integer, nullable=True)
    max_goal = db.Column(db.Integer, nullable=True)
    timeframe = db.Column(db.Enum('day', 'week', name='timeframe'),
                          nullable=True)
    # ---------- success metrics ----------
    current_week_success = db.Column(db.Float, nullable=True)
    last_week_success = db.Column(db.Float, nullable=True)
    total_success = db.Column(db.Float, nullable=True)

    user = db.relationship('User', backref=db.backref('habits'))

    def __repr__(self):
        """Representation of a habit."""
        return '<Habit {} user={}>'.format(self.title, self.user_id)

    # ---------- dates / times ----------

    def get_local_creation_timestamp(self):
        """Gets creation timestamp in user's timezone."""
        return self.user.convert_utc_to_local(self.created)

    def get_days_since_creation(self):
        """Gets number of days since habit was created."""
        creation_date = self.get_local_creation_timestamp().date()
        today = self.user.current_arrow().date()
        return (today - creation_date).days

    # ---------- success ----------

    def _get_relevant_completions(self):
        """Gets relevant completions used to calculate recent success."""
        if self.timeframe == 'day':
            yesterday = self.user.current_arrow().replace(days=-1).date()
            return [c for c in self.completions if
                    c.get_local_timestamp().date() == yesterday]
        else:
            # weekly habits
            week_ago = self.user.current_arrow().replace(days=-7).date()
            return [c for c in self.completions if
                    c.get_local_timestamp().date() > week_ago]

    def _get_relevant_weekday(self):
        """Gets day of the week as integer to use for success calculations.
        Sunday is 1, Saturday is 7."""
        weekday = self.user.current_arrow().weekday() + 2
        if weekday > 7:
            # this will make sunday 1 instead of 8
            weekday = weekday - 7
        return weekday

    def calculate_latest_success(self):
        """Calculates user's success over 1 timeframe iteration."""
        if not self.timeframe:
            # user doesn't have any success goals
            return None

        comps = self._get_relevant_completions()

        if self.max_goal:
            min_goal = self.min_goal or 0
            if len(comps) >= min_goal and len(comps) <= self.max_goal:
                return 1
            return 0

        else:
            if len(comps) > self.min_goal:
                # don't get over 100%
                return 1
            # gets percentage completed
            return len(comps) / float(self.min_goal)


class Completion(db.Model):
    """A completion of a habit by a user."""
    __tablename__ = 'completions'

    completion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.habit_id'),
                         nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    habit = db.relationship('Habit', backref=db.backref('completions'))

    def __repr__(self):
        """Representation of a completion."""
        return '<Completion {} habit={}>'.format(self.completion_id,
                                                 self.habit_id)

    # ---------- dates / times ----------

    def get_local_timestamp(self):
        """Gets timestamp in user's timezone."""
        return self.habit.user.convert_utc_to_local(self.timestamp)


# -------------------- helpers --------------------

def hash_password(password):
    """Generates salted SHA256 hash."""
    return pbkdf2_sha256.encrypt(password)


# -------------------- database setup --------------------

def connect_to_db(app, uri='lvlup'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + uri
    # suppresses unneeded warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
