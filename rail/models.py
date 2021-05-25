from .extensions import db
from flask_login import UserMixin

class Passenger(db.Model,UserMixin):

    __tablename__='passenger'
    Passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(2))
    address = db.Column(db.String(200))
    phone_no=db.Column(db.BigInteger,unique=True)
    Category=db.Column(db.String(20))
    Password=db.Column(db.String(120))
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

    def get_id(self):
        return (self.Passenger_id)

class Ticket(db.Model):

    __tablename__='ticket'
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


class Trains(db.Model):

    __tablename__='Trains'
    Train_No=db.Column(db.Integer)
    Train_Name=db.Column(db.String(60))
    SEQ=db.Column(db.Integer)
    Station_Code=db.Column(db.String(4),primary_key=True)
    Station_Name =db.Column(db.String(40))
    Arrival=db.Column(db.Time)
    Departure=db.Column(db.Time)
    Distance=db.Column(db.Integer)
    Source_Station_Code=db.Column(db.Integer)
    Source_Station_Name=db.Column(db.String(40))
    Destination_Station_Code=db.Column(db.Integer)
    Destination_Station_Name=db.Column(db.String(40))


    def __repr__(self):
        return '<Train : %r>' % self.Train_No

# def __init__(self, Train_No, Train_Name, SEQ,Station_Code,Station_Name,Arrival,Departure,Distance,Source_Station_Code,Source_Station_Name,Destination_Station_Code,Destination_Station_Name):
#     self.Train_No = Train_No
#     self.Train_Name = Train_Name
#     self.SEQ = SEQ
#     self.Station_Code = Station_Code
#     self.Station_Name = Station_Name
#     self.place_of_Departure = place_of_Departure
#     self.place_of_Arrival = place_of_Arrival
#     self.cost_of_ticket = cost_of_ticket
#     self.PNR=PNR
#     self.Passengerid=Passengerid
#     self.Train_Class=Train_Class

