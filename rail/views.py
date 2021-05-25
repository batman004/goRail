#FLASK IMPORTS :
from flask import Blueprint,render_template,redirect,request,flash,url_for
from .models import Ticket,Passenger
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from flask_login import login_user, login_required, logout_user, current_user

#EXTRA IMPORTS :
from datetime import datetime
import calendar
import random
import pickle
import pandas as pd
import warnings 
warnings.filterwarnings("ignore")
#from send_mail import send_mail

import numpy as np
data = pd.read_csv('rail/trainsxx.csv')
trainsno = data['Train No'].unique()
stations = data['Station Name'].unique()
stations = np.array(stations)

#-----------------------------------------------------------------------------

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html',user=current_user)

@views.route('/passenger',methods=["GET","POST"])
@login_required
def passenger():
    #query data from database about passenger : name, email ..... and train data

    pdata=Passenger.query.filter_by(Passenger_id=current_user.Passenger_id).first()
    
    print(current_user.Passenger_id)

    name=pdata.name
    email=pdata.email
    age=pdata.age
    gender=pdata.gender
    address=pdata.address
    phoneno=pdata.phone_no
    category=pdata.Category
    ppid=pdata.Passenger_id


    tdata=Ticket.query.filter_by(Passengerid=ppid).first()
    if tdata is not None:

        tname=tdata.Train_Name
        Date_of_T=tdata.Date_of_travel
        Time_of_Departure=tdata.Time_of_departure
        Time_of_arrival=tdata.Time_of_arrival
        D_From=tdata.place_of_Departure
        A_at=tdata.place_of_Arrival
        tcost=tdata.cost_of_ticket
        tpnr=tdata.PNR
    
        return render_template('passenger.html',name=name,email=email,age=age,gender=gender,address=address,phoneno=phoneno,category=category,tname=tname,dat=Date_of_T,timed=Time_of_Departure,timea=Time_of_arrival,pd=D_From,pa=A_at,cost=tcost,pnr=tpnr,tcheck=True)

    else:

        return render_template('passenger.html',user=current_user,name=name,email=email,age=age,gender=gender,address=address,phoneno=phoneno,category=category,tcheck=False)

@views.route('/cancel1',methods=["POST","GET"])
@login_required
def cancel1():
    if request.method == 'POST':


        pnr=request.form["pnr"]

        # ADD error handling to validate PNR 

        return redirect(url_for('cancel2',pnr=pnr, **request.args))#error='You have already Signed up !'
    return render_template('cancel.html')

@views.route('/cancel2',methods=["GET","POST"])
def cancel2():

    pnr=request.args['pnr']
    if request.method == 'POST':
        choice=request.form['yes_no']
        print(choice)
        if choice=="yes":
            tdata=Ticket.query.filter_by(PNR=pnr).first()

            #print(tdata.all())

            db.session.delete(tdata)
            db.session.commit()
        

            flash("Ticket Cancelled")
        else:

            return redirect(url_for('passenger'))#error='You have already Signed up !'



        return render_template('cancel1.html')
    return render_template('cancel1.html')


@views.route('/bookTicket', methods=["GET","POST"])
@login_required
def booking():


    data = pd.read_csv('rail/trainsxx.csv')

    error=None
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
        pickle_in = open("rail/ticketprices.pickle", "rb")
        linear = pickle.load(pickle_in)
        inputt=[train_t ,train_c ,fare_t ,month ,day ,weekday ,dur,route]  #check this tuple and manupulate input
        inputt = np.asarray(inputt,dtype='float64')
        inputt.reshape(-1,1)

        if(concession=="General"):
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

        #sprint(lst)

        #def __init__(self, Train_Name, Concession, Date_of_travel,Time_of_departure,Time_of_arrival,place_of_Departure,place_of_Arrival,cost_of_ticket,PNR,Passengerid,Train_Class):
       
        
        #print(data2)
        if(current_user.is_authenticated):

            pdata=Passenger.query.filter_by(Passenger_id=current_user.Passenger_id).first()

            ppid=pdata.Passenger_id

            # data2= Ticket(trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc)
            # db.session.add(data2)
            # db.session.commit()
            LST=[trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc]
            #return redirect(url_for('success',data=y.to_html(), pnr=pnr,**request.args,login_checker=login_checker))#error='You have already Signed up !'
            return redirect(url_for('views.success',data=y.to_html(),trainn=trainn,concession=concession,date=date,time_of_dep=time_of_dep,time_of_arr=time_of_arr,p_departure=p_departure,p_arrival=p_arrival,cost=cost,pnr=pnr,ppid=ppid,trainc=trainc ,**request.args,user=current_user))#error='You have already Signed up !'
            
        else:
            flash('Please Login First !')
            return render_template("successbooking.html")


    return render_template("bookTicket3.html",user=current_user)

@views.route('/success',methods=["GET","POST"])
@login_required
def success():

    data=request.args['data']
    trainn=request.args['trainn']
    concession=request.args['concession']
    date=request.args['date']
    time_of_dep=request.args['time_of_dep']
    time_of_arr=request.args['time_of_arr']
    p_departure=request.args['p_departure']
    p_arrival=request.args['p_arrival']
    cost=request.args['cost']
    pnr=request.args['pnr']
    ppid=request.args['ppid']
    trainc=request.args['trainc']

    LST=[trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc]
    print(LST)

    pdata=Passenger.query.filter_by(Passenger_id=current_user.Passenger_id).first()

    pemail=pdata.email
    pname=pdata.name
    msg=''
    #print(daata)
    if request.method == "POST":
        choice=request.form['yes_no']
        print(choice)
        if choice=="yes":
            # pdata=Passenger.query.filter_by(name=login_checker).first()

            # ppid=pdata.Passenger_id

            data2= Ticket(trainn, concession,date,time_of_dep,time_of_arr ,p_departure,p_arrival,cost,pnr,ppid,trainc)
            db.session.add(data2)
            db.session.commit()
            msg= f"Here are your Ticket Details :\n  Name :{pname} \n Train : {trainn} \n Date : {date}\n Time of Departure : {time_of_dep} \nTime of Arrival : {time_of_arr}\n Departure : {p_departure}\n Arrivaal : {time_of_arr}\n Cost : {cost}\nPNR : {pnr} "
            print(msg)
            # sendmail(msg,pemail)
            return render_template("successbooking.html",choice=choice,pnr=pnr)
        else:

            return redirect(url_for('views.booking'))#error='You have already Signed up !'
 
    return render_template('itenary2.html',data=data,cost=cost)

@views.route('/costPredictor',methods=["GET","POST"])
def costPredictor():
    
    global login_checker

    def convert_to_int(word):
        word_dict = {
            'Super Fast' : 1, 
            'Passenger Train' : 2, 
            'Express Train' : 3, 
            'INTERCITY' : 4, 
            'MD-LD' : 5, 
            'MD': 6, 
            'LD-MD' : 7,
            0 : 0
        }
        return word_dict[word]

    def convert_to_intt(word):
        word_dict = {
            '1AC' : 1, 
            '2AC' : 2, 
            'SL' : 3, 
            '1AC Plus' : 4,
            0 : 0
        }
        return word_dict[word]

    error=None
    if request.method == 'POST':
        p_departure = request.form['departure']
        p_arrival = request.form['arrival']
        date = request.form['date']
        train_class=request.form['trainClass']
        train_type=request.form['trainType']
        concession = request.form['concession']
        fare_t=request.form.get('fareType')
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
        pickle_in = open("rail/ticketprices.pickle", "rb")
        linear = pickle.load(pickle_in)
        inputt=[train_t ,train_c ,fare_t ,month ,day ,weekday ,dur,route]  #check this tuple and manupulate input
        inputt = np.asarray(inputt,dtype='float64')
        inputt.reshape(-1,1)

        if(concession=="General"):
            cp=linear.predict([inputt])[0]*4
        elif(concession=="Senior Citizen"):
            cp=linear.predict([inputt])[0]*4.0 -60

        else:
            cp=linear.predict([inputt])[0]*4.0 -40

        cost=int(cp)
        

        op='Predicted Ticket Price: ' +  "Rs." + str(cost)
        #print ('Predicted Ticket Price: \n', "Rs.",cp)
        return render_template('costPredictor3.html',op=op,user=current_user)

    return render_template('costPredictor3.html',user=current_user)
