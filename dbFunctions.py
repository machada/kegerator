from app import app
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

db = SQLAlchemy(app)

class BeerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beerName = db.Column(db.String(80), unique=False, nullable = False)
    breweryName = db.Column(db.String(80), unique=False, nullable = False)
    purchaseDate = db.Column(db.DateTime, unique=False, nullable = False)
    abv = db.Column(db.Float, unique=False, nullable = False)
    kegLine = db.Column(db.Integer, unique=False, nullable = False)
    initialVolume = db.Column(db.Float, unique=False, nullable = False)
    currentVolume = db.Column(db.Float, unique=False, nullable = False)
    status = db.Column(db.String(80), unique=False, nullable = False)
    kickDate = db.Column(db.DateTime, unique=False, nullable = True)
    beertrans = db.relationship('BeerTransactions', backref='beerPoured')

class BeerTransactions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    decrementVolume = db.Column(db.Float, unique=False, nullable = False)
    transDate = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable = False)
    beer_list_id = db.Column(db.Integer, db.ForeignKey('beer_list.id'))

class TempReadings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sensorNum = db.Column(db.Integer, unique=False, nullable = False)
    tempReading = db.Column(db.Float, unique=False, nullable = False)
    rhReading = db.Column(db.Float, unique=False, nullable = False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable = False)

class SensorStatus(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    currentStatus = db.Column(db.String(10), unique=False, nullable = False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable = False)

    
def addBeer(beerName, purchaseDate, abv, kegLine, initialVolume, currentVolume, status, kickDate, breweryName):
    newBeer = BeerList(beerName=beerName, purchaseDate=purchaseDate, abv=abv, kegLine=kegLine, initialVolume=initialVolume, currentVolume=currentVolume, status=status, kickDate=kickDate, breweryName=breweryName)
    db.session.add(newBeer)
    db.session.commit()
    #set previous beer occupying keg line to kicked status
    terminateBeer(kegLine)
    
    

def addTransaction(beer_list_id, decrementVolume):
    newTransaction = BeerTransactions(beer_list_id=beer_list_id, decrementVolume=decrementVolume)
    db.session.add(newTransaction)
    db.session.commit()
    results = db.session.query(BeerTransactions).all()
    resulting = db.session.query(BeerList).filter(BeerList.id==beer_list_id)

    stmt = db.session.query(BeerList).get(beer_list_id)
    stmt.currentVolume = stmt.currentVolume - decrementVolume
    db.session.commit()

    #print(resulting[0].beerName, resulting[0].currentVolume)

def terminateBeer(kegLine):
    results = db.session.query(BeerList).filter(BeerList.kegLine==kegLine, BeerList.status=='active')

    for r in results:
        max = 1
        test = r.id
        #print('active beers on line are ', r.beerName)

        if test > max:
            max = test

        r.status = 'kicked'
        r.kickDate = datetime.utcnow()

    newActive = db.session.query(BeerList).get(max)
    newActive.status = 'active'
    newActive.kickDate = '12/1/2200'
    db.session.commit()
    
def purchaseReport(startDate, endDate):
    reportOutput = db.session.query(BeerList).filter(BeerList.purchaseDate > startDate, BeerList.purchaseDate < endDate)
    
    #for r in reportOutput:
    #    print(r.beerName)
    
    return reportOutput

def getActiveBeer(kegLine):
    activeBeer = db.session.query(BeerList).filter(BeerList.status == 'active', BeerList.kegLine == kegLine)
    #print('active beer id is ',activeBeer[0].id, ' beer name ',activeBeer[0].beerName, ' amount left ', activeBeer[0].currentVolume)
    return activeBeer[0]


def addTemp(sensorNum, tempReading, rhReading, timeStamp):
    newReading = TempReadings(sensorNum=sensorNum, tempReading=tempReading, rhReading=rhReading, timeStamp=timeStamp )
    db.session.add(newReading)
    db.session.commit()
    print(newReading)
    
def getTempData(sensorNum, qtyReadings):
    lastRecord = db.session.query(TempReadings).order_by(TempReadings.id.desc()).first()
    lastID = lastRecord.id
    startID = lastID - (qtyReadings*3)
    tempSet = db.session.query(TempReadings).filter(TempReadings.id > startID).filter(TempReadings.sensorNum == sensorNum).order_by(TempReadings.id.asc()).limit(qtyReadings*3)
    #print("length is ",tempSet.count())
    #print("start id is ",startID, " last id is ",lastID)
    #for r in tempSet:
        #print('id is ',r.timeStamp, 'id is ',r.id, ' sensor num is ',r.sensorNum,' temp rd ',r.tempReading)
        #print('hello')


    output = createTempDict(tempSet,sensorNum)
    #print("the first temp in dict is ",output['tempL'][0])
    #print("the complete list is ",output['tempL'])

    return output

def createTempDict(queryData, sensorNum):
    #tempDict = {}
    #tempDict["rhReadings"] = [50,55,45,60,65]
    
    tempList = []
    rhList = []
    timeStamp = []
    

    for r in queryData:
        tempList+= [r.tempReading]
        rhList+= [r.rhReading]
        timeStamp+=[r.timeStamp]

    #print('print tempList ',tempList, rhList, timeStamp)
    outputDict = {}
    outputDict["sensorNum"] = sensorNum
    outputDict["tempL"] = tempList
    outputDict["rhL"] = rhList
    outputDict["timeStamp"] = timeStamp
    #print('outputdict is ',outputDict["timeStamp"])
    return outputDict
    
def getLastTemp():
    lastRecord = db.session.query(TempReadings).order_by(TempReadings.id.desc()).first()
    lastDateTime = lastRecord.timeStamp
    return lastDateTime

def newSensorStatus(status):
    newStatus = SensorStatus(currentStatus= status)
    db.session.add(newStatus)
    db.session.commit()
    print(newStatus)

def getLastSensorStatus():
    lastRecord = db.session.query(SensorStatus).order_by(SensorStatus.id.desc()).first()
    lastStatus = lastRecord.currentStatus
    return lastStatus