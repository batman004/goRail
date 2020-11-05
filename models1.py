# def __repr__(self):
#         return '<User %r>' % self.username

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Booking(db.Model):
    __tablename__ = 'Passenger_Data'
    booking_id=db.Column(db.Integer,primary_key=True)
    Date_of_booking=db.Column(db.DateTime)
    Train_No=db.Column(db.Integer,db.ForeignKey('train.Train_No'))
    PNR=db.Column(db.BigInteger,db.ForeignKey('ticket.PNR'))
    departure=db.Column(db.String(30))
    arrival=db.Column(db.String(30))
    main_data=db.Column(db.Integer,db.ForeignKey('Passenger.Passenger_id'),unique=True)
    
    def __repr__(self):
        return '<Booking %r>' % self.booking_id

class Train(db.Model):
    __tablename__='Train'
    Train_No=db.Column(db.Integer,primary_key=True)
    Train_Name=db.Column(db.String(30),unique=True)
    passengers=db.relationship('Passengers',backref='on_train')
    stn_ID=db.Column(db.String(4),db.ForeignKey('station.stn_code'))

    def __repr__(self):
        return '<Train %r>' % self.Train_No


class Ticket:
    __tablename__='Ticket'
    PNR=db.Column(db.Integer,primary_key=True)
    Class=db.Column(db.String(30),unique=True)
    Date_of_travel=db.Column(db.Date)
    Cost=db.Column(db.Integer)
    Time_of_departure=db.Column(db.Time)
    Time_of_arrival=db.Column(db.Time)
    pnr=db.relationship('Passengers',backref='pnr')

    def __repr__(self):
        return '<Ticket %r>' % self.PNR

    
class Station:
    __tablename__='Station'
    stn_code=db.Column(db.String(4),primary_key=True)
    stn_name=db.Column(db.String(30),unique=True)
    trains=db.relationship('Train',backref="passing_through")

    def __repr__(self):
        return '<Station %r>' % self.stn_code

            

# class Category:
#     cat_name=db.Column(db.String(20),primary_key=True)
#     Passengers_id=db.relationship('Passengers',backref="Category")

#new class with username, password & email , 
class Passenger():
    Passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(2))
    address = db.Column(db.String(200))
    phone_no=db.Column(db.BigInteger,unique=True)
    Category=db.Column(db.String(20))
    Password=db.Column(db.String(40))
    train=db.relationship('Booking',backref='Train_Data',uselist=False)

    def __repr__(self):
        return '<Passenger  %r>' % self.Passenger_id

    

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








































