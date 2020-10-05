import Adafruit_DHT
import time
import threading
import timeFunctions
import datetime
import dbFunctions

#pins 18, 4, 23

def startSensor(pinNumber,interval,sensorNum, sampleTotal):
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = pinNumber

    
    print("inside sampling call with pin number ",pinNumber)
    count = 0
    qtyReadings = 0
    sumTemp=0
    sumRH=0
    avgTemp = 0
    avgRH = 0
    
    while count < sampleTotal:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        count+=1
        print('inside while loop and count is ',count,' temp is ',temperature)
        if humidity is not None and temperature is not None:
            temperature = (temperature * 9/5)+32
            sumTemp = sumTemp + temperature
            sumRH = sumRH + humidity
            qtyReadings+=1
            print("sensor number ",pinNumber, ' count is ',count)
            #print("Temp={0:0.1f}C Humidity={1:0.1f}% ".format(temperature, humidity))
        else:
            counter = 0
            #print("sensor failure. Check wiring. sensor num ",pinNumber);
        time.sleep(interval)
        print('interval is ', interval)

    if qtyReadings > 0:
        avgTemp = round((sumTemp/qtyReadings),1)
        avgRH = round((sumRH/qtyReadings),1)
        logTime = timeFunctions.roundTime(datetime.datetime.now(),datetime.timedelta(minutes=5))
        dbFunctions.addTemp(sensorNum, avgTemp, avgRH, logTime)
        print('writing to db')
        print('logging values ', sensorNum, ' avg temp ', avgTemp, ' avgRH ',avgRH, ' log time ',logTime)

    mins = 3
    minCount = 0

    #while minCount < mins:
        #sampling(pinNumber,interval, sensorNum)
        #minCount = minCount + 5
        #print('next functioncall')

startSensor(4,3,1,20)