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


def _get_relevant_weekday_int(habit):
    """Gets day of the week as integer to use for calculations.
    Sunday is 1, Saturday is 7."""
    # weekday method returns monday as 0 and sunday as 6
    weekday = habit.user.current_arrow().weekday() + 2
    if weekday > 7:
        # this will make sunday 1 instead of 8
        weekday = weekday - 7
    return weekday


def _get_already_counted_weekdays(current_weekday):
    """Gets number of weekdays already counted in current_week."""
    # recording yesterday's now, so already counted rest of week
    counted = current_weekday - 2
    if counted <= 0:
        # there can be 1-6 days already counted
        counted = 6 + counted
    return counted


def _calculate_weekly_metrics_for_daily_habit(habit, latest):
    """Calculates current week's rating; sets up for new week if Sunday."""
    weekday = _get_relevant_weekday_int(habit)
    days_counted = _get_already_counted_weekdays(weekday)
    total_week_success = habit.current_week_success * days_counted
    total_week_success += latest
    current_week_success = total_week_success / (days_counted + 1)

    if weekday == 1:
        # it's sunday, so set up for the new week
        habit.last_week_success = current_week_success
        habit.current_week_success = 0

    else:
        habit.current_week_success = current_week_success


def calculate_success():
    """Calculates most recent success for habits.
    Calculated at midnight for habit's user's timezone."""
    habits = Habit.query.filter(Habit.timeframe.isnot(None)).all()

    for habit in habits:
        if not habit.user._is_midnight():
            # only calculate success if it's between midnight & 1
            continue

        latest = habit.calculate_latest_success()
        total = habit.total_success or 0

        if habit.user._is_sunday() and habit.timeframe == 'week':
            # time to calculate last week's success for weekly habit
            habit.last_week_success = latest
            # denominator will be total # of weeks habit has existed
            denominator = ceil(habit.get_days_since_creation() / 7.0)

        elif habit.timeframe == 'week':
            # only need to calculate past week success on sundays
            continue

        else:
            # denominator will be the number of days counting yesterday
            denominator = (habit.get_days_since_creation() - 1) or 1
            _calculate_weekly_metrics_for_daily_habit(habit, latest)

        habit.total_success = (latest + total) / float(denominator)

    db.session.commit()


schedule.every().hour.do(calculate_success)


while True:
    schedule.run_pending()
    # check every half-hour
    time.sleep(1800)
