#This file is where we will create database models 
from . import db
from flask_login import UserMixin #to work with flask login

#This table stores each user, their ID, Email, Password and Memorable Phrase
class User(db.Model, UserMixin):
    #Primary key will be an ID that auto increments
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    memorable_phrase = db.Column(db.String(200))
    # Tells flask to link diagrams with user
    chord_diagrams = db.relationship("ChordDiagram")
    chord_sheets = db.relationship("ChordSheet")

#This table stores each user's chord diagrams
class ChordDiagram(db.Model):
    #Primary key auto increments
    id = db.Column(db.Integer, primary_key=True)
    #Link the ChordDiagrams and User tables
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #Main data
    chord_name = db.Column(db.String(150))
    chord_data = db.Column(db.JSON)

#This table stores each user's chord sheets
class ChordSheet(db.Model):
    #Primary key auto increments
    id = db.Column(db.Integer, primary_key=True)
    #Link the ChordDiagrams and User tables
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #Main data
    song_name = db.Column(db.String(150))
    artist = db.Column(db.String(150))
    album = db.Column(db.String(150))
    difficulty = db.Column(db.String(50))
    tuning = db.Column(db.String(50))
    capo = db.Column(db.String(50))
    key = db.Column(db.String(50))
    bpm = db.Column(db.String(50))
    strumming_pattern = db.Column(db.String(300))
    lyrics_chords = db.Column(db.String(1000))
    notes = db.Column(db.String(300))

    
  
  






