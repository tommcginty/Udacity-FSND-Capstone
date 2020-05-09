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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # test movie
        self.new_movie = {
            'title': 'Test Title',
            'genre': 'Comedy',
            'relese_date': '2038/01/19'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])
        self.assertTrue(len(data["movies"]))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/movies?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resourse not found')

    def test_get_individual_movie(self):
        movie = Movie.query.first()
        res = self.client().get(f'/movies/{movie.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["title"], movie.title)

    def test_delete_movie(self):
        movies_before_delete = len(Movie.query.all())
        movie = Movie.query.order_by(Movie.id.desc()).first()
        res = self.client().delete(f'/movies/{movie.id}')
        data = json.loads(res.data)

        movies_after_delete = len(Movie.query.all())
        deleted_movie = Movie.query.filter(Movie.id == movie.id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(movies_after_delete == movies_before_delete - 1)
        self.assertEqual(deleted_movie, None)




if __name__ == "__main__":
    unittest.main()