def pourEvent(pinNumber, kegLine):
    import RPi.GPIO as GPIO
    import time
    import dbFunctions
    from datetime import datetime
    print("hello*********************************************************")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    try:
        pourAmount = 0
        count = 0
        count2 = 0
        while True:
            count = count + 1
            if GPIO.input(pinNumber) ==0:
                count2 += 1
            else:
                #print("closed")
                pourAmount = pourAmount + .0005943871
            if count > 10000:
                break
    finally:
        print("pour amount on kegline ",kegLine, " is ", pourAmount, "***********************************************************************")
        GPIO.cleanup()

    beerID = dbFunctions.getActiveBeer(kegLine)

    if pourAmount > 0:
        dbFunctions.addTransaction(beerID, pourAmount)