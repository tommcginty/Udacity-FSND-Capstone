import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from models import setup_db, db_drop_and_create_all, calculate_age, current_date, Movie, Actor
from auth.auth import AuthError, requires_auth



RESULTS_PER_PAGE = 6

def paginate_results(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * RESULTS_PER_PAGE
  end = start + RESULTS_PER_PAGE

  results = [result.format() for result in selection]
  current_results = results[start:end]
  
  return current_results

def create_app():
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  @TODO uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
  #db_drop_and_create_all()

  @app.route('/')
  def welcome():
    return 'Welcome to Central Casting'

#  Movies
#  ----------------------------------------------------------------  
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):
    try:
      movies = Movie.query.all()
      current_movies = paginate_results(request, movies)
      total_movies = len(movies)

      if len(current_movies) == 0:
        abort(404)

      return jsonify ({
          'success': True,
          'movies': current_movies,
          'total_movies': total_movies
        })
    except:
        abort(404)

  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('get:movies')
  def display_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    try:
      return jsonify({
        'success': True,
        'id': movie.id,
        'title': movie.title,
        'genre': movie.genre,
        'release_date': movie.release_date
      })
    except:
      abort(422)


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    try:
      movie.delete()
      return jsonify({
        'success': True,
        'deleted': movie_id,
      })
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def add_movie(jwt):
    movie = request.get_json()
    if not movie['title']:
      abort(400)
    new_movie = Movie(
      title = movie.get('title'),
      genre = movie.get('genre'),
      release_date = movie.get('release_date'),
    )
    try:
      Movie.insert(new_movie)
      return jsonify({
        'movie': movie,
        'success': True,
      })
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    original_title = movie.title
    if not movie:
      abort(404)
    updated_movie = request.get_json()

    title = updated_movie.get('title')
    genre = updated_movie.get('genre')
    release_date = updated_movie.get('release_date')

    if title:
      movie.title = title
    if genre:
      movie.genre = genre
    if release_date:
      movie.release_date = release_date
    try:
      movie.update()
      new_title = movie.title
      return jsonify({
        'success': True,
      }), 200
    except Exception as e:
      print('My exception occurred, value:', e)
      abort(422)
    
#  Actors
#  ----------------------------------------------------------------  
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt):
    try:
      actors = Actor.query.all()
      current_actors = paginate_results(request, actors)
      total_actors = len(actors)

      if len(current_actors) == 0:
        abort(404)
      
      return jsonify ({
          'success': True,
          'actors': current_actors,
          'total_actors': total_actors
        })
    except:
        abort(404)

  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def display_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    age = calculate_age(actor.birthdate)

    if actor is None:
      abort(404)
    try:
      return jsonify({
        'success': True,
        'id': actor.id,
        'name': actor.name,
        'gender': actor.gender,
        'age': age
      })
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    try:
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': actor_id,
      })
    except:
      abort(422)


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def add_actor(jwt):
    actor = request.get_json()
    if not actor['name']:
      abort(400)
    new_actor = Actor(
      name = actor.get('name'),
      gender = actor.get('gender'),
      birthdate = actor.get('birthdate'),
    )
    try:
      Actor.insert(new_actor)
      return jsonify({
        'actor': actor,
        'success': True,
      })
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not actor:
      abort(404)
    updated_actor = request.get_json()

    name = updated_actor.get('name')
    gender = updated_actor.get('gender')
    birthdate = updated_actor.get('birthdate')

    if name:
      actor.name = name
    if gender:
      actor.gender = gender
    if birthdate:
      actor.birthdate = birthdate
    try:
      actor.update()
      return jsonify({
        'success': True,
        'name': actor.name,
        'gender': actor.gender,
        'birthdate': actor.birthdate
      }), 200
    except Exception as e:
      print('My exception occurred, value:', e)
      abort(422)

# Error Handlers
#  ---------------------------------------------------------------- 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resourse not found'
    }), 404

  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
      }), 422
  
  @app.errorhandler(AuthError)
  def unauthorized(error):
      return jsonify({
          'success': False, 
          'error': error.status_code,
          'message': 'unauthorized'
          }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    