import threading
import tempsensors
import flowmeter

def startNow():
    #assumes 3 temp sensors on pins 18,4,23 respectively. 2 flowmeters on pins 17,5
    tempSensor1 = threading.Thread(target=tempsensors.startSensor, args=(18,3,1,100))
    tempSensor2 = threading.Thread(target=tempsensors.startSensor, args=(4,3,2,100))
    tempSensor3 = threading.Thread(target=tempsensors.startSensor, args=(23,3,3,100))

    flowSensor1 = threading.Thread(target=flowmeter.pourEvent, args=(17,1))
    flowSensor2 = threading.Thread(target=flowmeter.pourEvent, args=(5,2))


    tempSensor1.start()
    tempSensor2.start()
    tempSensor3.start()
    #flowSensor1.start()
    #flowSensor2.start()

#startNow()