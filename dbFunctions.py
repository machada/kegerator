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

    print(resulting[0].beerName, resulting[0].currentVolume)

def terminateBeer(kegLine):
    results = db.session.query(BeerList).filter(BeerList.kegLine==kegLine, BeerList.status=='active')

    for r in results:
        max = 1
        test = r.id
        print('active beers on line are ', r.beerName)

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
    
    for r in reportOutput:
        print(r.beerName)
    
    return reportOutput