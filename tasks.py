import os
import schedule
import time
from math import ceil
from twilio.rest import TwilioRestClient
from models import *
from server import app

tsid = os.environ['TWILIO_SID']
tauth = os.environ['TWILIO_AUTH']
tnum = os.environ['TWILIO_NUMBER']
twilio_client = TwilioRestClient(tsid, tauth)
connect_to_db(app)


def calculate_success():
    """Calculates most recent success for habits.
    Calculated at midnight for habit's user's timezone."""
    habits = Habit.query.filter(Habit.timeframe.isnot(None)).all()

    for habit in habits:
        if not habit.user._is_midnight():
            # only calculate success if it's between midnight & 1
            continue

        latest = habit._calculate_latest_success()
        total = habit.total_success or 0

        if habit.user._is_sunday() and habit.timeframe == 'week':
            # time to calculate last week's success for weekly habit
            habit.last_week_success = latest
            # denominator will be total # of weeks habit has existed
            denominator = ceil(habit._get_days_since_creation() / 7.0)

        elif habit.timeframe == 'week':
            # only need to calculate past week success on sundays
            continue

        else:
            # denominator will be the number of days counting yesterday
            denominator = (habit._get_days_since_creation() - 1) or 1
            habit._calculate_midweek_metrics(latest)

        habit.total_success = (latest + total) / float(denominator)

    db.session.commit()


def calculate_user_success():
    """Calculates user's total success for the past week.
    Calculated on Sundays at midnight in user's timezone."""
    users = User.query.all()
    for user in users:
        if not user._is_midnight() or not user._is_sunday():
            # only count on sundays at midnight
            continue
        user.last_week_success = user._calculate_past_week_success()
    db.session.commit()


schedule.every().hour.do(calculate_success)
schedule.every().hour.do(calculate_user_success)


while True:
    schedule.run_pending()
    # check every half-hour
    time.sleep(1800)
