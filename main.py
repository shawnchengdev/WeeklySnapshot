import sleep_duration_calculator
import time

#The date inwhich the user will be sent the email
#For Day, Monday is 1 and Sunday is 7
scheduled_date = {"Day": 5, "Hour": 16, "Minute": 0, "Second": 0}

while True:
    time.sleep(sleep_duration_calculator.get_sleep_duration(scheduled_date))
    time.sleep(2) #TEMPORARY prevents loop from returning at the same time
    print("\nAwoken")
