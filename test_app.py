import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

class CastingTestCase(unittest.TestCase):
    """This class represents the casting agenct test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = os.environ['TESTDB_URL']
        setup_db(self.app, self.database_path)

        # test movie
        self.new_movie = {
            'title': 'Untitled Action Movie',
            'genre': 'Action',
            'release_date': '2038/01/19'
        }

        # test actor
        self.new_actor = {
            'name': 'Jane Doe',
            'gender': 'Female',
            'birthdate': '1999/12/31'
        }
        # roles
        self.assistant = os.getenv('ASSISTANT')
        self.director = os.getenv('DIRECTOR')
        self.producer = os.getenv('PRODUCER')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
# Movie Tests
#---------------------------------------------------------------------------------------
    def test_get_paginated_movies(self):
        res = self.client().get('/movies', headers={'Authorization': self.assistant})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])
        self.assertTrue(len(data["movies"]))
    
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/movies?page=100', headers={'Authorization': self.assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resourse not found')

    def test_get_individual_movie(self):
        movie = Movie.query.first()
        res = self.client().get(f'/movies/{movie.id}', headers={'Authorization': self.assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["title"], movie.title)
    
    def test_add_movie(self):
        movies_before_addition = len(Movie.query.all())
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.producer})
        data = json.loads(res.data)
        movies_after_addition = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movies_after_addition == movies_before_addition + 1)

    def test_add_movie_unauthorized(self):
        movies_before_addition = len(Movie.query.all())
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.assistant})
        data = json.loads(res.data)
        movies_after_addition = len(Movie.query.all())

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')
        self.assertTrue(movies_after_addition == movies_before_addition)
        
    def test_400_empty_add_movie_with_no_title(self):
        movies_before_addition = len(Movie.query.all())
        no_title = {
            'title': '',
            'genre': 'Action',
            'release_date': '1900/01/01'
        }
        res = self.client().post('/movies', json=no_title, headers={'Authorization': self.producer})
        data = json.loads(res.data)
        movies_after_addition = len(Movie.query.all())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(movies_after_addition == movies_before_addition)

    def test_update_movie(self):
        movie = Movie.query.order_by(Movie.id.desc()).first()
        updated_movie = {'title': 'Untitled Comedy Movie', 'genre': 'Comedy', 'release_date': '2038/01/01'}
        res = self.client().patch(f'/movies/{movie.id}', json=updated_movie, headers={'Authorization': self.director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        movies_before_delete = len(Movie.query.all())
        movie = Movie.query.order_by(Movie.id.desc()).first()
        res = self.client().delete(f'/movies/{movie.id}', headers={'Authorization': self.producer})
        data = json.loads(res.data)

        movies_after_delete = len(Movie.query.all())
        deleted_movie = Movie.query.filter(Movie.id == movie.id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(movies_after_delete == movies_before_delete - 1)
        self.assertEqual(deleted_movie, None)

    def test_delete_movie_unauthorized(self):
        movies_before_delete = len(Movie.query.all())
        movie = Movie.query.order_by(Movie.id.desc()).first()
        res = self.client().delete(f'/movies/{movie.id}', headers={'Authorization': self.director})
        data = json.loads(res.data)

        movies_after_delete = len(Movie.query.all())
        deleted_movie = Movie.query.filter(Movie.id == movie.id).one_or_none()
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(movies_after_delete == movies_before_delete)
        self.assertEqual(deleted_movie.id, movie.id)

# Actor Tests
#---------------------------------------------------------------------------------------

    def test_get_paginated_actors(self):
        res = self.client().get('/actors', headers={'Authorization': self.assistant})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])
        self.assertTrue(len(data["actors"]))
    
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')
    
    def test_get_individual_actor(self):
        actor = Actor.query.first()
        res = self.client().get(f'/actors/{actor.id}', headers={'Authorization': self.assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["name"], actor.name)
    
    def test_add_actor(self):
        actors_before_addition = len(Actor.query.all())
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.producer})
        data = json.loads(res.data)
        actors_after_addition = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actors_after_addition == actors_before_addition + 1)

    def test_add_actor_unauthorized(self):
        actors_before_addition = len(Actor.query.all())
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.assistant})
        data = json.loads(res.data)
        actors_after_addition = len(Actor.query.all())

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')
        self.assertTrue(actors_after_addition == actors_before_addition)
        
    def test_400_empty_add_actor_with_no_name(self):
        actors_before_addition = len(Actor.query.all())
        no_name = {
            'name': '',
            'gender': 'Male',
            'birthdate': '1900/01/01'
        }
        res = self.client().post('/actors', json=no_name, headers={'Authorization': self.producer})
        data = json.loads(res.data)
        actors_after_addition = len(Actor.query.all())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(actors_after_addition == actors_before_addition)

    def test_update_actor(self):
        actor = Actor.query.order_by(Actor.id.desc()).first()
        original_name = actor.name
        updated_name = {'name': 'Jane Q Public'}
        res = self.client().patch(f'/actors/{actor.id}', json=updated_name, headers={'Authorization': self.director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        actors_before_delete = len(Actor.query.all())
        actor = Actor.query.order_by(Actor.id.desc()).first()
        res = self.client().delete(f'/actors/{actor.id}', headers={'Authorization': self.producer})
        data = json.loads(res.data)

        actors_after_delete = len(Actor.query.all())
        deleted_actor = Actor.query.filter(Actor.id == actor.id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(actors_after_delete == actors_before_delete - 1)
        self.assertEqual(deleted_actor, None)

    def test_delete_actor_unauthorized(self):
        actors_before_delete = len(Actor.query.all())
        actor = Actor.query.order_by(Actor.id.desc()).first()
        res = self.client().delete(f'/actors/{actor.id}', headers={'Authorization': self.assistant})
        data = json.loads(res.data)

        actors_after_delete = len(Actor.query.all())
        deleted_actor = Actor.query.filter(Actor.id == actor.id).one_or_none()
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(actors_after_delete == actors_before_delete)
        self.assertEqual(deleted_actor.id, actor.id)


if __name__ == "__main__":
    unittest.main()