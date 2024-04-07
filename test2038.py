# ==================================
#           test2038.py
# ----------------------------------
# Written by G.D. Walters
# ==================================

import machine
import utime
import time
from time import sleep, localtime, gmtime
import sys
import gc

from datetime import MAXYEAR, MINYEAR, datetime, date, timedelta, timezone, tzinfo
    
# Simulate datetime to be January 19, 2038 03:14:00 UTC
def settime2038():
    tm=utime.gmtime(timelong)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
                    
# Return a local time based using datetime module datetime.datetime.now(timezone)                    
def showMyTime():
    import datetime
    my_timezone=timezone(timedelta(hours=-5))
    current_time = datetime.datetime.now(my_timezone)
    return current_time
    
timelong=2147483639  # January 19, 2038 03:14:00 UTC

# Do a garbage collect
gc.collect()
# Set the machine.RTC to Jan 19, 2038 03:14:00 UTC
settime2038()
print(f"{gmtime()=} - {showMyTime()=}")
#print(showMyTime())

while True:

    print(f"{gmtime()=} - {showMyTime()=}")
    #print(showMyTime())    
    time.sleep(1)