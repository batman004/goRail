from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    P_data=db.relationship('Ticket',backref='Passenger_Data',uselist=False,null=True)

    def __init__(self, name, email, age,gender,address,phone_no,Category,Password):
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.address = address
        self.phone_no = phone_no
        self.Category = Category
        self.Password = Password
















class Ticket(db.Model):

    __tablename__='Ticket'
    PNR=db.Column(db.Integer,primary_key=True)
    Train_Class=db.Column(db.String(30),unique=True)
    Train_Name=db.Column(db.String(60))
    Concession=db.Column(db.String(30))
    Date_of_travel=db.Column(db.Date)
    Cost=db.Column(db.Integer)
    Time_of_departure=db.Column(db.Time)
    Time_of_arrival=db.Column(db.Time)
    place_of_Departure =db.Column(db.String(40))
    place_of_Arrival=db.Column(db.String(40))
    cost_of_ticket=db.Column(db.Integer)
    Passengerid=db.Column(db.Integer,db.ForeignKey('passenger.Passenger_id'))

    def __init__(self, Train_Class, Train_Name, Concession, Date_of_travel,Cost,Time_of_departure,Time_of_arrival,place_of_Departure,place_of_Arrival,cost_of_ticket,Passengerid):
        self.Train_Class = Train_Class
        self.Train_Name = Train_Name
        self.Concession = Concession
        self.Date_of_travel = Date_of_travel
        self.Cost = Cost
        self.Time_of_departure = Time_of_departure
        self.Time_of_arrival = Time_of_arrival
        self.place_of_Departure = place_of_Departure
        self.place_of_Arrival = place_of_Arrival
        self.cost_of_ticket = cost_of_ticket
        self.Passengerid=Passengerid
























# class Passenger(db.Model):
#     __tablename__='passengers'
#     Passenger_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True)
#     email = db.Column(db.String(200))
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String(2))
#     address = db.Column(db.String(200))
#     phone_no=db.Column(db.BigInteger,unique=True)
#     Category=db.Column(db.String(20))
#     Password=db.Column(db.String(40))
#     train=db.relationship('Booking',backref='Train_Data',uselist=False)

#     def __init__(self, name, email, age,gender,address,phone_no,Category,Password):
#         self.name = name
#         self.email = email
#         self.age = age
#         self.gender = gender
#         self.address = address
#         self.phone_no = phone_no
#         self.Category = Category
#         self.Password = Password



# class Booking(db.Model):
#     __tablename__ = 'Booking_data'
#     booking_id=db.Column(db.Integer,primary_key=True)
#     Date_of_booking=db.Column(db.DateTime)
#     Train_No=db.Column(db.Integer,db.ForeignKey('train.Train_No'))
#     PNR=db.Column(db.BigInteger,db.ForeignKey('ticket.PNR'))
#     departure=db.Column(db.String(30))
#     arrival=db.Column(db.String(30))
#     main_data=db.Column(db.Integer,db.ForeignKey('passenger.Passenger_id'),unique=True)
    
#     def __init__(self, Date_of_booking, Train_No, PNR,departure,arrival,main_data):
#         self.Date_of_booking = Date_of_booking
#         self.Train_No = Train_No
#         self.PNR = PNR
#         self.departure=departure
#         self.arrival=arrival
#         self.main_data=main_data



# class Station(db.Model):
#     __tablename__='Station'
#     stn_code=db.Column(db.String(4),primary_key=True)
#     stn_name=db.Column(db.String(30),unique=True)
#     trains=db.relationship('Train',backref="passing_through")


# class Train(db.Model):
#     __tablename__='Train'
#     Train_No=db.Column(db.Integer,primary_key=True)
#     Train_Name=db.Column(db.String(30),unique=True)
#     passengers=db.relationship('Booking',backref='on_train')
#     stn_ID=db.Column(db.String(4),db.ForeignKey('station.stn_code'))

#     def __init__(self, Train_Name, stn_ID):
#         self.Train_Name = Train_Name
#         self.stn_ID = stn_ID


# class Ticket(db.Model):
#     __tablename__='Ticket'
#     PNR=db.Column(db.Integer,primary_key=True)
#     Class=db.Column(db.String(30),unique=True)
#     Date_of_travel=db.Column(db.Date)
#     Cost=db.Column(db.Integer)
#     Time_of_departure=db.Column(db.Time)
#     Time_of_arrival=db.Column(db.Time)
#     pnr=db.relationship('Booking',backref='pnr')

#     def __init__(self, Class, Date_of_travel, Cost, Time_of_departure,Time_of_arrival):
#         self.Class = Class
#         self.Date_of_travel = Date_of_travel
#         self.Cost = Cost
#         self.Time_of_departure = Time_of_departure
#         self.Time_of_arrival = Time_of_arrival

 
# class Category:
#     cat_name=db.Column(db.String(20),primary_key=True)
#     Passengers_id=db.relationship('Passengers',backref="Category")

#new class with username, password & email , 

    

# class Passengers(db.Model):
#     __tablename__ = 'Passenger_Data'
#     Passenger_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True)
#     email = db.Column(db.String(200))
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String(2))
#     address = db.Column(db.String(200))
#     phone_no=db.Column(db.BigInteger,unique=True)
#     Date_of_booking=db.Column(db.Timestamp)
#     Train_No=db.Column(db.Integer,db.ForeignKey('train.Train_No'))
#     Category=db.Column(db.String(20),db.ForeignKey('category.cat_name'))
#     PNR=db.Column(db.BigInteger,db.ForeignKey('ticket.PNR'))
#     Password=db.Column(db.String(40))
#     login=db.relationship('Signup',backref='Login_Creds',uselist=False)
