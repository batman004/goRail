from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Passenger
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login',methods=["POST","GET"])
def login():
    error=None
    if request.method == 'POST':
        passenger_email=request.form['email']
        passenger_password=request.form['password']
        # add check for already existing user or not and check if password matches
        exists = db.session.query(Passenger.Passenger_id).filter_by(email=passenger_email).scalar()
        print(exists)
        
        if exists is not None:

            pdata=Passenger.query.filter_by(email=passenger_email).first()
            pswd_check=check_password_hash(pdata.Password,passenger_password)  
            print(pswd_check)
        
            if pswd_check is True:

                login_user(pdata, remember=True)

                flash('You were successfully logged in')
            else:
                flash('Please enter Correct password')
                return render_template('login.html')
        else:
            flash("Please enter correct credentials")
            return render_template('login.html')

        #return redirect(url_for('/home',login_checker=login_checker,**request.args))
        return redirect(url_for('views.index'))
    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    login_checker="Login"
    logout_user()
    flash('You were successfully logged out !')
    return redirect(url_for('views.index'))


@auth.route('/signUp',methods=["POST","GET"])
def signup():

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
        hashed_pswd = generate_password_hash(password) 
        
        if db.session.query(Passenger.Passenger_id).filter_by(email=passenger_email).count() == 0:
            data= Passenger(passenger_name, passenger_email, passenger_age,passenger_gender, passenger_address,passenger_phoneno,passenger_category ,hashed_pswd)
            db.session.add(data)
            db.session.commit()
            login_user(data, remember=True)
            flash('Successfully Signed Up !')
            return redirect(url_for('views.index'))

        else:
            error='You have already Signed up using this email !'
            return render_template('signUp2.html',error=error)
 
    return render_template('signUp2.html',user=current_user)

