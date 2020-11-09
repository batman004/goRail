#-------------------------------------imports------------------------------

from flask import Flask,render_template,redirect,request,flash,url_for

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import calendar

#from passlib.hash import pbkdf2_sha256
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


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:uvpostgres269@localhost/gorail2'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


db = SQLAlchemy(app)

#----------------------------------------DATABASE CLASSES----------------


class Passenger(db.Model):

    __tablename__='passenger'
    Passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(2))
    address = db.Column(db.String(200))
    phone_no=db.Column(db.BigInteger,unique=True)
    Category=db.Column(db.String(20))
    Password=db.Column(db.String(40))
    P_data=db.relationship('Ticket',backref='Passenger_Data',uselist=False)

    def __init__(self, name, email, age,gender,address,phone_no,Category,Password):
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.address = address
        self.phone_no = phone_no
        self.Category = Category
        self.Password = Password

# class Train(db.Model):
#     __tablename__='trains'
#     train_no=db.Column(db.Integer,primary_key=True)
#     train_name=db.Column(db.VARCHAR(20))
#     seq=db.Column(db.Integer)
#     station_code=db.Column(db.VARCHAR(4))
#     station_name=db.Column(db.VARCHAR(40))
#     arrival_time=db.Column(db.Time)
#     departure_time =db.Column(db.Time, primary_key=True)
#     distance=db.Column(db.Integer)
#     source_station=db.Column(db.VARCHAR(4))
#     source_station_name=db.Column(db.VARCHAR(40))
#     destination_station=db.Column(db.VARCHAR(4))
#     destination_station_name=db.Column(db.VARCHAR(40))

#     def __init__(self, train_no, train_name, seq,station_code,station_name,arrival_time,departure_time,distance,source_station,source_station_name,destination_station,destination_station_name):
#         self.train_no = train_no
#         self.train_name = train_name
#         self.seq = seq
#         self.station_code = station_code
#         self.station_name = station_name
#         self.arrival_time = arrival_time
#         self.departure_time = departure_time
#         self.distance = distance
#         self.source_station = source_station
#         self.source_station_name = source_station_name
#         self.destination_station = destination_station
#         self.destination_station_name = destination_station_name




class Ticket(db.Model):

    __tablename__='Ticket'
    ticket_id=db.Column(db.Integer,primary_key=True)
    #Train_Class=db.Column(db.String(10))
    Train_Name=db.Column(db.String(60))
    Concession=db.Column(db.String(30))
    Date_of_travel=db.Column(db.Date)
    Time_of_departure=db.Column(db.Time)
    Time_of_arrival=db.Column(db.Time)
    place_of_Departure =db.Column(db.String(40))
    place_of_Arrival=db.Column(db.String(40))
    cost_of_ticket=db.Column(db.Integer)
    PNR=db.Column(db.BigInteger)
    Passengerid=db.Column(db.Integer,db.ForeignKey('passenger.Passenger_id'))
    Train_Class=db.Column(db.String(10))

    #Train_Type=db.Column(db.String(30))
    #train_data=db.Column(db.Integer,ForeignKey('train.train_no'))


    def __init__(self, Train_Name, Concession, Date_of_travel,Time_of_departure,Time_of_arrival,place_of_Departure,place_of_Arrival,cost_of_ticket,PNR,Passengerid,Train_Class):
        self.Train_Name = Train_Name
        self.Concession = Concession
        self.Date_of_travel = Date_of_travel
        self.Time_of_departure = Time_of_departure
        self.Time_of_arrival = Time_of_arrival
        self.place_of_Departure = place_of_Departure
        self.place_of_Arrival = place_of_Arrival
        self.cost_of_ticket = cost_of_ticket
        self.PNR=PNR
        self.Passengerid=Passengerid
        self.Train_Class=Train_Class




#-----------------------------------Routes------------------------------


login_checker="Login"



@app.route('/')
def index():
    global login_checker 

    #login_checker="Login"    
    return render_template('index.html',login_checker=login_checker)#,login_checker="Login"

@app.route('/home')
def home():
    #global login_checker
    login_checker=request.args['login_checker']
    
    return render_template('index.html',login_checker=login_checker)



@app.route('/login',methods=["POST","GET"])
def login():
    error=None
    global login_checker 
    if request.method == 'POST':
        passenger_email=request.form['email']
        passenger_password=request.form['password']
        # add check for already existing user or not and check if password matches
        exists = db.session.query(Passenger.Passenger_id).filter_by(email=passenger_email).scalar()
        print(exists)
        pswd=db.session.query(Passenger.Password==passenger_password).filter_by(Password=passenger_password).scalar()
        print(pswd)
        if exists is not None and pswd is not None:
        
            name = Passenger.query.filter_by(email=passenger_email).first()
            login_checker=name.name
            flash('You were successfully logged in')
        else:
            flash("Please enter correct credentials")
            return render_template('login.html')

        return redirect(url_for('home',login_checker=login_checker,**request.args))
    return render_template('login.html')


@app.route('/logout')
def logout():
    global login_checker
    login_checker="Login"
    flash('You were successfully logged out !')

    return redirect(url_for('home',login_checker=login_checker,**request.args))
    


@app.route('/signUp',methods=["POST","GET"])
def signup():
    #login_checker="Login"
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
        #hashed_pswd = sha256_crypt.hash('password') 
        login_checker=passenger_name


        #print(passenger_name, passenger_email, passenger_phoneno, password)
        if passenger_name == '' or passenger_email == '' or password == '' or passenger_email == '' or passenger_gender==''  or passenger_address == '' or passenger_age=='':
            error = 'Enter data in all feilds. Please try again!'
            return render_template('signUp2.html',error=error)
        
        if db.session.query(Passenger.Passenger_id).filter_by(name=passenger_name).count() == 0:
            data= Passenger(passenger_name, passenger_email, passenger_age,passenger_gender, passenger_address,passenger_phoneno,passenger_category ,password)
            db.session.add(data)
            db.session.commit()
            flash('Successfully Signed Up !')
            login_checker=passenger_name
            # global passenger_name
            return redirect(url_for('home',login_checker=login_checker, **request.args))#error='You have already Signed up !'

            #send_mail(customer, dealer, rating, comments)
        
    return render_template('signUp2.html')
        # if db.session.query(Signup).filter(Passengers.name == passenger_name).count() == 0:


@app.route('/passenger',methods=["GET","POST"])
def passenger():
    #query data from database about passenger : name, email ..... and train data

    global login_checker

    pdata=Passenger.query.filter_by(name=login_checker).first()

    name=pdata.name
    email=pdata.email
    age=pdata.age
    gender=pdata.gender
    address=pdata.address
    phoneno=pdata.phone_no
    category=pdata.Category
    ppid=pdata.Passenger_id



    tdata=Ticket.query.filter_by(Passengerid=ppid).first()
    
    tname=tdata.Train_Name
    Date_of_T=tdata.Date_of_travel
    Time_of_Departure=tdata.Time_of_departure
    Time_of_arrival=tdata.Time_of_arrival
    D_From=tdata.place_of_Departure
    A_at=tdata.place_of_Arrival
    tcost=tdata.cost_of_ticket
    tpnr=tdata.PNR
   

    return render_template('passenger.html',name=name,email=email,age=age,gender=gender,address=address,phoneno=phoneno,category=category,tname=tname,dat=Date_of_T,timed=Time_of_Departure,timea=Time_of_arrival,pd=D_From,pa=A_at,cost=tcost,pnr=tpnr)
    #return render_template('passenger.html',login_checker=login_checker,name=name,email=email,age=age,gender=gender,address=address,phoneno=phoneno,category=category)




@app.route('/bookTicket', methods=["GET","POST"])
def booking():
    global login_checker 


    data = pd.read_csv('trainsxx.csv')


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
        concession = request.form['concession']
        train_class=request.form['trainClass']
        train_type=request.form['trainType']

        trainc=train_class
        #train_type1=train_type
        #Passenger_id=request.form['Passenger_id']
        #print(p_departure, p_arrival, date, concession)


            
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

        #pnr = random.randint(10000000, 99999999)


        if(p_departure=="DELHI-SAFDAR" and p_arrival=="AGRA CANTT"):
            route=1
        elif(p_departure=="AGRA CANTT" and p_arrival=="DELHI-SAFDAR"):
            route =2
        elif(p_departure=="SAWANTWADI R" and p_arrival=="MADGOAN JN."):
            route=3
        else:
            route =4

        fare_t=1
        x=datetime.strptime(date,"%Y-%m-%d")
        month=x.month
        day=x.day
        weekday=x.weekday()
        
        train_c=convert_to_intt(train_class)
        train_t=convert_to_int(train_type)
        dur=160
        pickle_in = open("ticketprices.pickle", "rb")
        linear = pickle.load(pickle_in)
        inputt=[train_t ,train_c ,fare_t ,month ,day ,weekday ,dur,route]  #check this tuple and manupulate input
        inputt = np.asarray(inputt,dtype='float64')
        inputt.reshape(-1,1)

        if(concession=="general"):
            cp=linear.predict([inputt])[0]*4
        elif(concession=="Senior Citizen"):
            cp=linear.predict([inputt])[0]*4.0 -60

        else:
            cp=linear.predict([inputt])[0]*4.0 -40


        cost=int(cp)

        y=data.loc[c1:c2, :]
        trainn=y['Train Name'].unique()[0]
        trainn=str(trainn)
        time_of_dep=y['Departure Time'].iloc[0]
        idx=y.index[y['Station Name']==p_arrival][0]
        time_of_arr=y['Arrival time'].loc[idx]
        pnr = random.randint(1000000, 9999999)

        # pdata=db.session.query(Passenger.Passenger_id).filter_by(name=login_checker).first()
        # print(pdata)
        pdata=Passenger.query.filter_by(name=login_checker).first()

        ppid=pdata.Passenger_id

        lst=[trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc]
        print(lst)

        #def __init__(self, Train_Name, Concession, Date_of_travel,Time_of_departure,Time_of_arrival,place_of_Departure,place_of_Arrival,cost_of_ticket,PNR,Passengerid,Train_Class):
       
        
        data2= Ticket(trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc)
        db.session.add(data2)
        db.session.commit()
        print(data2)
        return redirect(url_for('success',data=y.to_html(), pnr=pnr,**request.args,login_checker=login_checker))#error='You have already Signed up !'

    return render_template("bookTicket3.html",login_checker=login_checker)



@app.route('/success',methods=["GET","POST"])
def success():
    data=request.args['data']
    #print(daata)
    if request.method == "POST":
        choice=request.form['yes_no']
        print(choice)
        if choice=="yes":
            pnr=request.args['pnr']
            return render_template("successbooking.html",choice=choice,pnr=pnr)
        else:
            return redirect(url_for('booking'))#error='You have already Signed up !'
 
    return render_template('itenary2.html',data=data)




@app.route('/costPredictor',methods=["GET","POST"])
def costPredictor():
    
    global login_checker


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
            cp=linear.predict([inputt])[0]*4
        elif(concession=="Senior Citizen"):
            cp=linear.predict([inputt])[0]*4.0 -60

        else:
            cp=linear.predict([inputt])[0]*4.0 -40
        

        op='Predicted Ticket Price: ' +  "Rs." + str(cp)
        #print ('Predicted Ticket Price: \n', "Rs.",cp)
        return render_template('costPredictor3.html',op=op,login_checker=login_checker)

    return render_template('costPredictor3.html',login_checker=login_checker)


  

if __name__=='__main__':
    app.run() 
