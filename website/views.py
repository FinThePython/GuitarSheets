from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .models import ChordDiagram, ChordSheet
from . import db

#A blueprint file separates our routes out as you can define them all in here
views = Blueprint('views', __name__)

#This route directs to the home page
@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")


# --- Routes related to chord diagrams --- #


#This route directs to the page to VIEW CHORD DIAGRAMS
@views.route('/chord-diagrams') 
@login_required
def chord_diagrams(): 
    #Users will be able to view their chord diagrams here#
 
    return render_template("chord_diagrams.html")

#This route will be for getting the chord diagram data
@views.route('/get-chord-diagrams', methods=["GET","POST"])
@login_required
def get_chord_diagrams():
    #Get the chords THIS user has made by ID
    chords = ChordDiagram.query.filter_by(user_id = current_user.id).all()
    #This array will hold dictionaries of each chord's data
    chord_data = []
    #Add each chord dictionary into the array
    for chord in chords:
        #chords are added in dictionary form
        current_chord = {
            "chordName": chord.chord_name,
            "startingFret": chord.chord_data["startingFret"],
            "frettedPositions": chord.chord_data["frettedPositions"],
            "stringMarkers": chord.chord_data["stringMarkers"]
            }
        chord_data.append(current_chord)
    
    #Return the chord data to the font-end to draw in the chords with JS
    return chord_data

#This route directs to the page where the user can CREATE CHORD DIAGRAMS
@views.route('/create-chord-diagram', methods=["GET","POST"])
@login_required
def create_chord_diagrams():
    return render_template("create_chord_diagram.html", )

#This route is for SAVING CHORD DIAGRAMS
@views.route("/save-chord-diagram", methods = ["GET", "POST"])
@login_required
def save_chord_diagram():
    #Check for post request and get data with JSON 
    if request.method == "POST":
        #Get the chord data as a json
        chord_data = request.get_json()
        chord_name = chord_data["chordName"]
        starting_fret = chord_data["startingFret"]
        print(chord_data)

        #Check if chord already exists
        chord = ChordDiagram.query.filter_by(chord_name=chord_name, user_id = current_user.id).first()
        print(chord)
        if chord:
            flash("Chord name already in use!", category="error")
        
        #Validation checks
        elif chord_name == "":
            flash("Your chord needs a name!", category="error")
        elif starting_fret == "":
             flash("Your chord needs a starting fret!", category="error")

        #If chord is valid
        else:
            new_chord = ChordDiagram(user_id=current_user.id, chord_name=chord_name, chord_data=chord_data)
            db.session.add(new_chord)
            db.session.commit()
            flash("Your new chord has been saved!", category="success")
    
    #End function by sending an empty Array
    return []

#This route is for DELETING CHORD DIAGRAMS
@views.route('/delete-chord-diagram', methods = ["GET", "POST"])
@login_required
def delete_chord_diagrams():
    #Check for a post request and get the JSON data
    if request.method == "POST":
        chord_name = request.get_json()
        print(chord_name)

        #Find chord in db
        chord = ChordDiagram.query.filter_by(chord_name=chord_name, user_id = current_user.id).first()
        if chord:
            #If found delete the chord
            flash(f"Your chord  has been successfully deleted!", category="success")
            db.session.delete(chord)
            db.session.commit()
    
    return []
        
# --- Routes related to chord sheets --- #


#This route is for the chord diagrams main page
@views.route('/chord-sheets') 
@login_required
def chord_sheets():
    #Users will be able to search for their chord sheets be directed to a link to view them here
    return render_template("chord_sheets.html")

#This route is for creating the chord sheets
@views.route('/create-chord-sheet', methods = ["GET", "POST"])
@login_required
def create_chord_sheet():
    #Users will be able to fill out a form to make chord sheets here and the data will be saved to the db
    if request.method == "POST":
        #Get data from form on post request
        song_name = request.form.get("songName")
        artist = request.form.get("artist")
        album = request.form.get("album")
        difficulty = request.form.get("difficulty")
        tuning = request.form.get("tuning")
        capo = request.form.get("capo")
        key = request.form.get("key")
        bpm = request.form.get("bpm")
        strumming_pattern = request.form.get("strummingPatterns")
        lyrics_chords = request.form.get("lyricsChords")
        notes = request.form.get("notes")

        #Check if song is already in database otherwise add it 
        song = ChordSheet.query.filter_by(user_id = current_user.id, song_name=song_name, artist=artist, album=album).first()
        if song:
            flash("You already have a chord sheet for this song!", category="error")
        else:
            new_song = ChordSheet(
                user_id = current_user.id,
                song_name=song_name, artist=artist, album=album,
                difficulty=difficulty, tuning=tuning, capo=capo,
                key=key, bpm=bpm, strumming_pattern=strumming_pattern,
                lyrics_chords=lyrics_chords, notes=notes
            )
            db.session.add(new_song)
            db.session.commit()
            flash("Chord Sheet successfully created!", category='success')
            return redirect(url_for("views.chord_sheets"))
    return render_template("create_chord_sheet.html")

#This route will be for getting the chord sheet data
@views.route('/get-chord-sheets', methods=["GET","POST"])
@login_required
def get_chord_sheets():
    #Get the chord sheets THIS user has made by ID
    sheets = ChordSheet.query.filter_by(user_id = current_user.id).all()
    #This array will hold dictionaries of each sheet's data
    sheet_data = []
    #Add each sheet dictionary into the array
    for song in sheets:
        #sheets are added in dictionary form
        current_song = {
            "songName": song.song_name,
            "artist": song.artist,
            "difficulty": song.difficulty,
            "id": song.id
            }
        sheet_data.append(current_song)
    
    #Return the chord data to the font-end to draw in the chords with JS
    return sheet_data

#This route uses a dynamic URL to display chord sheets
@views.route('/view-chord-sheet/<int:sheet_id>')
@login_required
def view_chord_sheets(sheet_id):
    #Get song data from the database by ID 
    sheet = ChordSheet.query.filter_by(id = sheet_id, user_id = current_user.id,).first()

    #users are forbidden from accessing other people's chord sheets
    if sheet.user_id != current_user.id:
        abort(403)

    #Take sheet data as an object to pass into a static HTML file
    return render_template("view_chord_sheet.html", sheet = sheet)

#This route is for confirming to delete a chord sheet
@views.route("/delete-chord-sheet/<int:sheet_id>", methods = ["GET","POST"])
@login_required
def delete_chord_sheet(sheet_id):
    #Get song data from the database by ID 
    sheet = ChordSheet.query.filter_by(id = sheet_id, user_id = current_user.id,).first()

    #users are forbidden from accessing other people's chord sheets
    if sheet.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        #If the request IS confirmed to delete this sheet, remove it from db
        db.session.delete(sheet)
        db.session.commit()
        flash("Your Chord Sheet has been deleted", category="success")
        return redirect(url_for("views.chord_sheets"))
    
    #Render this page to confirm deletion 
    return render_template("delete_chord_sheet.html", sheet=sheet)
    
#This route is for confirming to delete a chord sheet
@views.route("/edit-chord-sheet/<int:sheet_id>", methods = ["GET","POST"])
@login_required
def edit_chord_sheet(sheet_id):
    #Get song data from the database by ID 
    sheet = ChordSheet.query.filter_by(id = sheet_id, user_id = current_user.id,).first()

    #users are forbidden from accessing other people's chord sheets
    if sheet.user_id != current_user.id:
        abort(403)

    #Update record 
    if request.method == "POST":
        sheet.song_name = request.form.get("songName")
        sheet.artist = request.form.get("artist")
        sheet.album = request.form.get("album")
        sheet.difficulty = request.form.get("difficulty")
        sheet.tuning = request.form.get("tuning")
        sheet.capo = request.form.get("capo")
        sheet.key = request.form.get("key")
        sheet.bpm = request.form.get("bpm")
        sheet.strumming_pattern = request.form.get("strummingPatterns")
        sheet.lyrics_chords = request.form.get("lyricsChords")
        sheet.notes = request.form.get("notes")

        db.session.commit()
        flash("Your Chord Sheet has been updated!", category="success")
        return redirect(url_for("views.view_chord_sheets", sheet_id=sheet.id))
    
    #Render this page to confirm deletion 
    return render_template("edit_chord_sheet.html", sheet=sheet)

