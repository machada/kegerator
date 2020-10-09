from time import time

#converts datetime value to hour minute for graphing
def strip(temps):
    timeList = []
    for times in temps["timeStamp"]:
        print(times.time().strftime('%H:%M'), ' printing times')
        timeList.append(times.time().strftime('%H:%M'))
        return timeList
        #print(temps["timeStamp"], " these are the times")

        