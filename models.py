import os
import json
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

database_path = os.environ.get('DATABASE_URL')
# To run locally, comment the line above and uncomment the line
#database_path = "postgres://postgres@localhost:5432/casting"

current_date = date.today()

db = SQLAlchemy()

'''
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def calculate_age(birthdate, current_date=current_date):
    ''' Calculates age based on an actors birthdate
    assumes birthdate is a string formated as YYYY/MM/DD '''
    birthday = datetime.strptime(birthdate, '%Y/%m/%d').date()
    #caclulates age based on days in the year - .2425 is to make up for leap years
    days_in_year = 365.2425
    age = int((current_date - birthday).days / days_in_year)
    return age

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    genre = db.Column(db.String)
    release_date = db.Column(db.String())

    def __repr__(self):
        return '<Title {}>'.format(self.title)

    def __init__(self, title, genre, release_date):
        self.title = title
        self.genre = genre
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'genre': self.genre,
        'release_date': self.release_date
        }
    
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    gender = db.Column(db.String(10))
    birthdate = db.Column(db.String())

    def __repr__(self):
        return '<Name {}>'.format(self.name)

    def __init__(self, name, gender, birthdate):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()   

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name' : self.name,
        'gender': self.gender,
        'age': calculate_age(self.birthdate)
        }

def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()

#This will initialize the database with a few records
def db_create_records():
    opera = Movie(title='A Night at the Opera', genre='Comedy', release_date='1935/11/15')
    duck_soup = Movie(title='Duck Soup', genre='Musical', release_date='1933/11/17')
    races = Movie(title='A Day at the Races', genre='Comedy', release_date='1937/06/11')

    groucho = Actor(name='Groucho Marx', gender='Male', birthdate='1890/10/02')
    harpo = Actor(name='Harpo Marx', gender='Male', birthdate='1888/09/23')
    chico = Actor(name='Chico Marx', gender='Male', birthdate='1887/10/02')

    Movie.insert(opera)
    Movie.insert(duck_soup)
    Movie.insert(races)
    Actor.insert(groucho)
    Actor.insert(harpo)
    Actor.insert(chico)