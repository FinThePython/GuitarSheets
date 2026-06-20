from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Database configuration
db = SQLAlchemy() #Declare database with SQLAlchemy 
DB_NAME = "guitar_sheets.db" #Declare database name

#This function creates the database only if it doesn't exist 
def create_database(app):
    db_path = path.join(app.root_path, DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("Created database!")

#Creates app 
def create_app(): 
    app = Flask(__name__)

    #Secret key for encryption 
    app.config['SECRET_KEY'] = 'alt0177pkadwDWki#@/3219'

    #Database initialization
    from .models import User
    from .models import ChordDiagram
    from .models import ChordSheet

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 
    create_database(app)

    #Flask login_manager set up 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #redirect if not logged in
    login_manager.init_app(app)

    #Flask will use this function to find the user's data in the db
    @login_manager.user_loader 
    def load_user(id):
        #looks for primary key
        return User.query.get(int(id))

    #import blueprints
    from .views import views
    from .auth import auth

    #register blueprints and any url_prefixes
    app.register_blueprint(views,url_prefix ='/')
    app.register_blueprint(auth,url_prefix ='/')

    return app
