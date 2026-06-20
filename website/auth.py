from flask import Blueprint, render_template, redirect, url_for, request, flash, redirect
from .models import User
from .import db
from pathlib import Path
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

#A blueprint file separates our routes out as you can define them all in here
auth = Blueprint('auth', __name__)

#This route directs to the login page with get and post requests enabled
@auth.route('/login', methods=["GET", "POST"])
def login():
    #user sends a post request to login
    if request.method == 'POST':
        #get data from form
        email = request.form.get('email')
        password = request.form.get('password')
        #finds user in db
        user = User.query.filter_by(email=email).first()
        #if user is found check if their password hashes match
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='success')
                login_user(user, remember=True) #remember that they are logged in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category = 'error')
        else:
            flash('Email does not exist.', category = 'error')  

    return render_template("login.html")

#Returns a list of unsafe passwords from a txt file for validation purposes 
def load_unsafe_passwords():
    #I used the pathlib library to give an absolute path to the static folder for a txt file of common passwords
    base_path = Path(__file__).resolve().parent
    file_path = base_path / "static" / "textFiles" / "500-worst-passwords.txt"
    with open(file_path,"r") as file:
        unsafe_passwords = file.read().splitlines()
    return unsafe_passwords
unsafe_passwords = load_unsafe_passwords()

#This route directs to the sign-up page, with get and post requests enabled 
@auth.route('/sign-up', methods=["GET", "POST"])
def signup():
    #If a post request is made, start processing a new attempt to sign-up
    if request.method == "POST":
        #Retrieve HTML form data 
        email = request.form.get("email") 
        memorable_phrase = request.form.get('memorablePhrase')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #check if user is already signed up or not 
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        
        #Sign-up validation
        elif len(email) < 5: #Email must be of valid length
            flash("Email must be greater than 4 characters.", category="error")
        elif len(memorable_phrase) <5: #Memorable Phrase must be of valid length
            flash("Memorable Phrase must be greater than 4 characters.", category="error")
        elif password1 in unsafe_passwords: #Password must not be too common
            flash("Password is too common", category="error")
        elif len(password1) <7: #Password must be of valid length
            flash("Password must be greater than 6 characters.", category="error")
        elif password1 != password2: #Password must be confirmed twice
            flash("Passwords don't match.", category="error")

        else: #Create new user if passed validation
            #Hash sensitive user info
            password = generate_password_hash(password1, method="pbkdf2:sha256")
            memorable_phrase = generate_password_hash(memorable_phrase, method="pbkdf2:sha256")
            #Declare new user
            new_user = User(email=email, password=password, memorable_phrase=memorable_phrase)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) #Tells flask to remember that the user has been logged in
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

#This route directs to the logout page
@auth.route('/logout')
@login_required #this route is only accessible if they are logged in
def logout():
    logout_user()
    flash('You have been logged out successfully!', category='success')
    return redirect(url_for("views.home"))

#This route directs to the password-reset page if they had forgotten their password 
@auth.route('/account-recovery', methods=["GET", "POST"])
def account_recovery():
    #user sends a post request 
    if request.method == 'POST':
        #get data from form
        email = request.form.get('email')
        memorable_phrase = request.form.get('memorablePhrase')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #Checks email
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found", category="error")
        #Checks memorable phrase
        elif not check_password_hash(user.memorable_phrase, memorable_phrase):
            flash("Memorable Phrase is incorrect.", category='error')
        #Checks password
        elif password1 in unsafe_passwords: #Password must not be too common
            flash("Password is too common.", category="error")
        elif password1 != password2: #Password must be confirmed twice
            flash("Passwords don't match.", category="error")
        elif len(password1) <7: #Password must be of valid length
            flash("Password must be greater than 6 characters.", category="error")
        else:
            #Change password in db
            new_password = generate_password_hash(password1, method="pbkdf2:sha256")
            user.password = new_password
            db.session.commit()
            flash("Your password has been reset successfully!", category="success")
            return redirect(url_for("auth.login"))

    return render_template("account_recovery.html")


