from flask import Flask, render_template, request, redirect, url_for, json, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, NumberRange, AnyOf
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
from wtforms.fields.html5 import DateField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Phoenix1@localhost/kegerator'
app.config['SECRET_KEY'] = 'Thisisasecret!'
nav = Nav(app)

import dbFunctions
import flowmeter
nav.register_element('my_navbar', Navbar(
    'thenav',
     View('Home Page','home'),
     View('Dashboard', 'dashboard'),
     View('Login', 'login'),
     View('Add New Beer', 'form')
))

#test git update
class LoginForm(FlaskForm):
    username = DateField('username', validators=[InputRequired('a user name is required'), Length(min=5, max=10, message="too long or too short")])
    password = DateField('password', validators=[InputRequired()])

class DashBoardForm(FlaskForm):
    startDate = DateField('Start Date',validators=[InputRequired('must enter dates')], format='%Y-%m-%d')
    endDate = DateField('End Date', validators=[InputRequired('must enter dates')], format='%Y-%m-%d')


class BeerInput(FlaskForm):
    breweryName = StringField('Brewery Name', validators=[InputRequired('Brewery Name field is required'), Length(min=3, max=30, message="enter value between 3 and 30 characters long")])
    beerName = StringField('Beer Name', validators=[InputRequired('a user name is required'), Length(min=3, max=30, message="enter value between 3 and 30 characters long")])
    abv = DecimalField('ABV', validators=[InputRequired('a user name is required'), NumberRange(min=1, max=100, message="must be number value between 1 and 100")])
    kegLine = IntegerField('Keg Line', validators=[InputRequired('a user name is required'), NumberRange(min=1, max=2, message="enter either 1 or 2")])
    kegSize = DecimalField('Keg Size', validators=[InputRequired('a user name is required'), NumberRange(min=1, max=100, message="must be number value between 1 and 100")])
    password = PasswordField('Password', validators=[InputRequired(),AnyOf('0000', message='pin doesnt match')])

class HomeForm(FlaskForm):
    kegLine = IntegerField('Enter the Keg Line to Decrement', validators=[InputRequired('a user name is required'), NumberRange(min=1, max=2, message="enter either 1 or 2")])

@app.route('/addBeer', methods=['GET', 'POST'])
def form():
    form = BeerInput()
    if request == 'POST':
        print('add beer post request')

    if form.validate_on_submit():
        beer_Name = form.beerName.data
        brewery_Name = form.breweryName.data
        incoming_abv = float(form.abv.data)
        inc_kegline = int(form.kegLine.data)
        keg_Size = float(form.kegSize.data)
        purchaseDate = datetime.utcnow()
        kick_Date = '12/1/2200'
        status = 'active'
        print('calling addbeer route')
        dbFunctions.addBeer(beer_Name, purchaseDate, incoming_abv, inc_kegline, keg_Size, keg_Size, status, kick_Date, brewery_Name)
        return redirect(url_for('form'))

    return render_template('form.html', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    form = DashBoardForm()
    output = 'some rando text'
    print(request.method)
    
    if request.method == 'POST':
        if form.startDate.data > form.endDate.data:
            print('start date bigger than end date')
            
        else:
            print('end date bigger than start date')
            output = dbFunctions.purchaseReport(form.startDate.data, form.endDate.data)
           
            
       

    return render_template('dashboard.html', form=form, output=output)

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/getChartData', methods=['GET','POST'])
def test():
    beer1 = (dbFunctions.getActiveBeer(1))
    beer2 = (dbFunctions.getActiveBeer(2))

    beer1Dict = {}
    beer1Dict["name"] = beer1.beerName
    beer1Dict["currentVolume"] = beer1.currentVolume * 8
    beer1Dict["amountConsumed"] = (beer1.initialVolume - beer1.currentVolume) * 8
    beer1Dict["kegLine"] = beer1.kegLine

    beer2Dict = {}
    beer2Dict["name"] = beer2.beerName
    beer2Dict["currentVolume"] = beer2.currentVolume * 8
    beer2Dict["amountConsumed"] = (beer2.initialVolume - beer2.currentVolume) * 8
    beer2Dict["kegLine"] = beer2.kegLine

    beerDictionary = {
        "beer1": beer1Dict,
        "beer2": beer2Dict
    }

    if request.method == 'GET':
        payload =  json.dumps(beerDictionary)
    return (payload)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    beer1 = (dbFunctions.getActiveBeer(1))
    beer2 = (dbFunctions.getActiveBeer(2))
    beerName1 = beer1.beerName
    beerName2 = beer2.beerName
    amountLeft1= beer1.currentVolume
    amountLeft2 = beer2.currentVolume

    if request.method == 'POST':
        #flowmeter.pourEvent(int(form.kegLine.data))
        dbFunctions.addTransaction( dbFunctions.getActiveBeer(form.kegLine.data).id, .5)
     
        def buildDB():
            iterations = 15
            increment = 4
            startingValue = 1
            currentValue = 1

            while (currentValue < iterations):
                startingValue = startingValue + increment
                currentValue = currentValue + 1
                dbFunctions.addTemp(3, startingValue)
                print(startingValue)

        buildDB()

            #dbFunctions.addTemp(1, 40)
        print('called flowmeter already')
        return redirect(url_for('home'))
    return render_template('home.html', form=form, beerName1=beerName1,beerName2=beerName2, amountLeft1=amountLeft1, amountLeft2=amountLeft2 )

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80, debug=False)