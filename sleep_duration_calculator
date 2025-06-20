import datetime

#takes in a dict of a specific time in the week, to then calculate the number of seconds remaining before reaching that specific time
def get_sleep_duration(schedule):
    current_time = datetime.datetime.now()
    current_time = current_time.replace(year = 1, month = 1, day = 1, microsecond = 0)     #Set to January first, since the real date isn't necessary

    scheduled_time = datetime.datetime(year = 1, month = 1, day = 1, hour = schedule["Hour"], minute = schedule["Minute"], second = schedule["Second"])

    #isoweekday() returns the weekday of the provided date as a number, Monday is 0, and Sunday is 6
    delta_weekday = schedule["Day"] - (datetime.datetime.now().weekday() + 1) #I didn't the weekday() by one because in schedule, monday is 1
    if (delta_weekday < 0 or (delta_weekday == 0 and current_time >= scheduled_time)):
        delta_weekday += 7

    scheduled_time = scheduled_time.replace(day = delta_weekday + current_time.day)

    difference = scheduled_time - current_time
    sleep_seconds = difference.total_seconds()
    print("Proceeding to sleep for", int(sleep_seconds/86400), "days,", int(sleep_seconds/3600) % 24, "hours,", int(sleep_seconds/60) % 60, "minutes and", sleep_seconds % 60, "seconds")
    return (sleep_seconds)
