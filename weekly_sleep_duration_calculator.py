import datetime


# Takes a dict with specific date in a week and calculates the number of seconds remaining before reaching that specific date
def get_sleep_duration(schedule:dict):
    current_date = datetime.datetime.now()

    # Sets to January first, since the real date isn't necessary, and it will allow us to disregard month sizes
    current_date = current_date.replace(year = 1, month = 1, day = 1, microsecond = 0)     
    scheduled_date = datetime.datetime(year = 1, month = 1, day = 1, hour = schedule["Hour"], minute = schedule["Minute"], second = schedule["Second"])

    # isoweekday() returns the weekday of the provided date as a number, Monday is 0, and Sunday is 6
    delta_weekday = schedule["Day"] - datetime.datetime.now().weekday()
    if (delta_weekday < 0 or (delta_weekday == 0 and current_date >= scheduled_date)):
        delta_weekday += 7

    # Setting scheduled_date's day to be the correct amount of days away from the current date
    scheduled_date = scheduled_date.replace(day = delta_weekday + current_date.day)

    difference = scheduled_date - current_date
    sleep_seconds = difference.total_seconds()

    # If it's the scheduled time, sleep_seconds will be set to 7 days
    if (sleep_seconds == 0):
        sleep_seconds = 604800

    print("Proceeding to sleep for", int(sleep_seconds/86400), "days,", int(sleep_seconds/3600) % 24, "hours,", int(sleep_seconds/60) % 60, "minutes and", sleep_seconds % 60, "seconds")
    return sleep_seconds
