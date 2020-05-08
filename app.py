import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from models import setup_db, db_drop_and_create_all

load_dotenv()

RESULTS_PER_PAGE = 6

def paginate_results(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * RESULTS_PER_PAGE
  end = start + RESULTS_PER_PAGE

  results = [question.format() for result in selection]
  current_results = results[start:end]
  
  return current_results

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  db_drop_and_create_all():

  @app.route('/')
  def welcome():
    return 'Welcome to Central Casting'

#  Movies
#  ----------------------------------------------------------------  

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    