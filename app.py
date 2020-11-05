#-------------------------------------imports------------------------------

from flask import Flask,render_template,redirect,request,flash,url_for

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import calendar

#from models import *
import random
import pickle
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import numpy as np
data = pd.read_csv('trainsxx.csv')
trainsno = data['Train No'].unique()
stations = data['Station Name'].unique()
stations = np.array(stations)


#-------------------------------configs--------------------------------------------

app=Flask(__name__)

app.secret_key = "thisisasecretkey"


# ENV = 'dev'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:uvpostgres269@localhost/gorail'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


#db = SQLAlchemy(app)


#-----------------------------------Routes------------------------------

@app.route('/')
def index():
    login_checker="Login"

    return render_template('index.html',login_checker=login_checker)#,login_checker="Login"

@app.route('/login',methods=["POST","GET"])
def login():
    error=None
    login_checker="Login"
    if request.method == 'POST':
        passenger_email=request.form['email']
        passenger_password=request.form['password']
        #add check for already existing user or not and check if password matches
        # exists = db.session.query(Signup.Passenger_id).filter_by(email=passenger_email).scalar()
        # pswd=db.session.query(Signup.Password==passenger_password).filter_by(email=passenger_email).scalar()
        # if exists is not None and pswd is not None:
        
            # name = Signup.query.filter_by(email=passenger_email).first()

        flash('You were successfully logged in')
        return redirect(url_for('index',login_checker=name.name))
    return render_template('login.html')



@app.route('/signUp',methods=["POST","GET"])
def signup():
    login_checker="Login"
    error=None
    if request.method == 'POST':
        passenger_name = request.form['Name']
        passenger_email = request.form['email']
        passenger_phoneno = request.form['phoneNumber']
        password = request.form['password']
        passenger_age=request.form['age']
        passenger_gender=request.form['gender']
        passenger_address=request.form['address']
        passenger_category=request.form['category']

        print(passenger_name, passenger_email, passenger_phoneno, password)
        if passenger_name == '' or passenger_email == '' or password == '' or passenger_email == '' or passenger_gender==''  or passenger_address == '' or passenger_age=='':
            error = 'Enter data in all feilds. Please try again!'
            return render_template('signUp2.html',error=error)
        
        # if db.session.query(Signup.Passenger_id).filter_by(name=passenger_name).count() == 0:
        #     data = Signup(passenger_name, passenger_email, passenger_age,passenger_gender, passenger_address,passenger_phoneno,passenger_category ,password)
        #     db.session.add(data)
        #     db.session.commit()
        #     #send_mail(customer, dealer, rating, comments)
        else:
            flash('Successfully Signed Up !')
            return redirect(url_for('index',login_checker=passenger_name, **request.args))#error='You have already Signed up !'

    return render_template('signUp2.html')
        # if db.session.query(Signup).filter(Passengers.name == passenger_name).count() == 0:



@app.route('/bookTicket', methods=["GET","POST"])
def booking():
    error=None
    if request.method == 'POST':
        p_departure = request.form['departure']
        p_arrival = request.form['arrival']
        date = request.form['date']
        concession = request.form['concession']
        print(p_departure, p_arrival, date, concession)

        # CHOICE = input("\nDo you want to buy ticket ? \n")
        # if CHOICE == 'y':
        #     pnr = random.randint(1000000000, 9999999999)
        #     PNR[x] = pnr
        #     print("Your PNR Number is: ", str(PNR[x]))
        #     Tickets[PNR[x]] = [cp, start, end]
        # else:
        #     print("Ticket not bought")

            
        c1 = 0
        c2 = 0

        for i in range(0, len(stations)):
            if p_departure == stations[i]:
                break
            else:
                c1 += 1

        for i in range(0, len(stations)):
            if p_arrival == stations[i]:
                break
            else:
                c2 += 1
        dist = abs((c2 - c1))*100 #calculating distances between stations

        x=data.loc[c1:c2, :]
        return render_template("itenary.html", data=x.to_html())

        if request.method == 'POST':
            choice=request.form['yes_no']
            print(choice)
            return render_template("successbooking.html",choice=choice)
        

    return render_template("bookTicket.html")



@app.route('/costPredictor',methods=["GET","POST"])
def costPredictor():



    def convert_to_int(word):
        word_dict = {'Super Fast':1, 'Passenger Train':2, 'Express Train':3, 'INTERCITY':4, 'MD-LD':5, 'MD': 6, 'LD-MD':7,0:0}
        return word_dict[word]


    def convert_to_intt(word):
        word_dict = {'1AC':1, '2AC':2, 'SL':3, '1AC Plus':4,0:0}
        return word_dict[word]



    error=None
    if request.method == 'POST':
        p_departure = request.form['departure']
        p_arrival = request.form['arrival']
        date = request.form['date']
        train_class=request.form['trainClass']
        train_type=request.form['trainType']
        concession = request.form['concession']
        fare_t=request.form['fare_type']
        print(p_departure, p_arrival, date,train_class, concession)


        if(fare_t=="Promo"):
            fare_t=1
        else:
            fare_t=2


        x=datetime.strptime(date,"%Y-%m-%d")
        month=x.month
        day=x.day
        weekday=x.weekday()

        train_c=convert_to_intt(train_class)
        train_t=convert_to_int(train_type)

        print(train_c,train_t)
        
#chosen 4 routes from db, for ML pred

        if(p_departure=="DELHI-SAFDAR" and p_arrival=="AGRA CANTT"):
            route=1
        elif(p_departure=="AGRA CANTT" and p_arrival=="DELHI-SAFDAR"):
            route =2
        elif(p_departure=="SAWANTWADI R" and p_arrival=="MADGOAN JN."):
            route=3
        else:
            route =4
            
        c1 = 0
        c2 = 0

        for i in range(0, len(stations)):
            if p_departure == stations[i]:
                break
            else:
                c1 += 1

        for i in range(0, len(stations)):
            if p_arrival == stations[i]:
                break
            else:
                c2 += 1
        dist = abs((c2 - c1))*100 #calculating distances between stations
        print(dist)
        dur=160
#importing ML Model
        pickle_in = open("ticketprices.pickle", "rb")
        linear = pickle.load(pickle_in)
        inputt=[train_t ,train_c ,fare_t ,month ,day ,weekday ,dur,route]  #check this tuple and manupulate input
        inputt = np.asarray(inputt,dtype='float64')
        inputt.reshape(-1,1)

        if(concession=="general"):
            cp=linear.predict([inputt])*4
        elif(concession=="Senior Citizen"):
            cp=linear.predict([inputt])*4.0 -60

        else:
            cp=linear.predict([inputt])*4.0 -40
        

        op='Predicted Ticket Price: ' +  "Rs." + str(cp)
        print ('Predicted Ticket Price: \n', "Rs.",cp)
        return render_template('costPredictor.html',op=op)

    return render_template('costPredictor.html')


  

if __name__=='__main__':
    app.run(debug=True)