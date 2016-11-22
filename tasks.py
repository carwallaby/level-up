import os
import schedule
import time
from random import choice
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

        if habit.user._is_sunday() and habit.timeframe == 'week':
            # time to calculate last week's success for weekly habit
            habit.last_week_success = latest

        elif habit.timeframe == 'week':
            # only need to calculate past week success on sundays
            continue

        else:
            habit._set_midweek_metrics(latest)

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


def create_sms():
    users = User.query.filter(User.reminders.isnot(None)).all()
    for user in users:
        if user.reminders == 'weekly' and not user._is_sunday():
            # only send weekly reminders on sundays
            continue
        if not user.habits:
            msg_body = 'Hey there! Remember to track your habits'
        else:
            habit = choice(user.habits).title
            msg_body = 'Have you completed {} today? Mark it'.format(habit)
        msg_body += ' in Level Up and see your progress!'

        try:
            client.messages.create(body=msg_body, to=user.sms_num, from_=tnum)
        except TwilioRestException as e:
            print e


schedule.every().hour.do(calculate_success)
schedule.every().hour.do(calculate_user_success)
schedule.every().day.at('18:00').do(create_sms)


while True:
    schedule.run_pending()
    # check every half-hour
    time.sleep(1800)
