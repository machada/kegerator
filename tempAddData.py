import timeFunctions
import dbFunctions
import datetime
import time

sensorNum = 3
tempReading = 60
rhReading = 65.9
timeStamp = datetime.datetime.now()
timeStamp1 = timeFunctions.roundTime(timeStamp,datetime.timedelta(minutes=5))

#dbFunctions.addTemp(sensorNum, tempReading, rhReading, timeStamp1)
#tempRecord = dbFunctions.getTempData(2,5)
#dbFunctions.getTempData(3,5)

#def addTemp(sensorNum, tempReading, rhReading, timeStamp):
sensorNum = 1

def add3Sensor():
    sNum = 0
    r=1
    x=1
    records = 5
    temp = 40
    rh = 53
    limit = 3
    timeStamp = datetime.datetime.now()
    timeStamp1 = timeFunctions.roundTime(timeStamp,datetime.timedelta(minutes=5))
    for x in range(0,3):
        sNum = sNum + 1
        for r in range(1,5):
            temp = temp + sNum
            rh = rh + (sNum/2)
            dbFunctions.addTemp(sNum, temp, rh, timeStamp1)
          
            print("inside loop")
            
        print("sensor is ",sNum)
add3Sensor()

