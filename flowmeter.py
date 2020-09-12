#import RPi.GPIO as GPIO
import time
import dbFunctions
from datetime import datetime




def pourEvent(kegLine):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    try:
        pourAmount = 0
        count = 0
        while True:
            count= count + 1
            if GPIO.input(18)==0:
                #each time the flowmeter rotates is equivalent to 2.25 ml, converted to gal we get .0005943871
                #print('open')
                print('low voltage and count is ', count)
                if count > 50000:
                    break
            
            else:
                #print("closed")
                pourAmount = pourAmount + .0005943871
                print('high voltage and count is reset', pourAmount)
                count = 0
        
    finally:
        GPIO.cleanup()
    print('total poured is ', pourAmount)
    beerID = dbFunctions.getActiveBeer(kegLine)
    dbFunctions.addTransaction(beerID, pourAmount)

