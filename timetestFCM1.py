# ==================================
#       timetestFCM1.py
# ----------------------------------
# Written by G.D. Walters
# ==================================

import machine
import port_ntptime
import utime
import network
#import ntptime
import secret
import time
from time import sleep, localtime, gmtime
import sys
import gc

from datetime import MAXYEAR, MINYEAR, datetime, date, timedelta, timezone, tzinfo

# Check that the board is a Pico-W with wireless support
def GetWhichPico():
    which1 = sys.implementation
    if "Pico W" in (sys.implementation[2]):
        print("Pico W")
        return True
    else:
        print("NOT Pico W")
        return False
    

def connectNetwork():
    global myipconfig

    # Setup onboard LED
    led=machine.Pin("LED",machine.Pin.OUT)
    led.off()
    # Setup Network
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    # Provide SSID and PASSWORD from secret.py file
    ap=secret.SSID
    pwd=secret.PASSWORD
    # Try to connect to the wireless network
    wlan.connect(ap,pwd)
    # Loop until we get connected
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect")
        time.sleep(1)
    # Print the status value and the ifconfig values
    print(wlan.status())
    print(wlan.ifconfig())
    myipconfig=wlan.ifconfig()
    # Turn on the onboard LED
    led.on()
    
def printFromTimestamp(ts):
    print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
def printHuman(use12Hr=True):
    rtc=machine.RTC()
    lt = rtc.datetime()
    print(f"{lt=}")
    #lt = localtime()
    hr = lt[4]
    offset = -5
    if hr < abs(offset):
        hr=(hr+24)+offset
    if use12Hr:
        if hr > 12:
            hr-=12
    fmtd=f"{lt[0]}-{lt[1]}-{lt[2]} {hr}:{lt[5]}:{lt[6]}"
    return fmtd
#import utime

def settime2(tz):
    t = time.time()
    if t < 0:
        return False
    else:
        tm = utime.gmtime(t)
        tm2= utime.localtime(t+tz)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        return True
                    
def showMyTime():
    import datetime
    my_timezone=timezone(timedelta(hours=-5))
    current_time = datetime.datetime.now(my_timezone)
    return current_time
    
timelong=2147483640

# def setTime(timezoneOffset):
#     import machine
#     import utime
#     import time
#     
#     t = time.time()
# 
#     tm = utime.gmtime(t)
# 
#     machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + timezoneOffset, tm[3], tm[4], tm[5], 0))
# 
cst=-6*3600
cdt=-5*3600
EPOCH = time.gmtime(0)[0]
print(f"{EPOCH=}")
rtc=machine.RTC()
dti=rtc.datetime()
print(f"{dti=}")

# Check to see if the Pico has network
which=GetWhichPico()
if which == False:
    sys.exit()
    
# Connect to the network    
connectNetwork()

    
loop = True
while loop:
    secs=port_ntptime.time()
        
        
    print(secs)
    if secs > 0:
        #print(secs)
        gc.collect()
        success=settime2(cdt)
        if success:
            loop = False
                
    else:
        sleep(2)
        
# Now print gmtime and localtime
print(f"{gmtime()=} - {localtime()=}")
print(showMyTime())

while True:
    print(showMyTime())
    time.sleep(10)