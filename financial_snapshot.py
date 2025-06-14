#Packages
import datetime
import time

#Print  just for an additional visual feedback on starting the code
print("Program Started")

#The date inwhich the user will be sent the email
#For Day, Monday is 1 and Sunday is 7
scheduled_date = {"Day": 3, "Hour": 16, "Minute": 0, "Second": 0}

#Loop indefinitely
while True:
    #Calculates the seconds between the current time and time scheduled to send a email
    start_date = datetime.datetime(year = 1, month = 1, day = 1, hour = datetime.datetime.now().hour, minute = datetime.datetime.now().minute, second = datetime.datetime.now().second)

    delta_day = scheduled_date["Day"] - datetime.date.today().isoweekday()
    if (delta_day < 0 or ((delta_day == 0 and start_date.hour >= scheduled_date["Hour"] and start_date.minute >= scheduled_date["Minute"]) and start_date.second >= scheduled_date["Second"])):
        delta_day += 7

    end_date = datetime.datetime(year = start_date.year, month = start_date.month, day = delta_day + start_date.day, hour = scheduled_date["Hour"], minute = scheduled_date["Minute"], second = scheduled_date["Second"])

    print("\nStart Time:\t", start_date)
    print("Wake Time\t", end_date)

    difference = end_date - start_date

    sleep_seconds = difference.total_seconds()
    print("Proceeding to sleep for", sleep_seconds, "seconds")

    time.sleep(sleep_seconds)

    #The program awakes and signals its awaking and the current time so we can confirm it awakening at the right time 
    print("\nAwoken at time:")
    print(datetime.datetime.now())

