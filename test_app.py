import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import setup_db, db, Movie, Actor
import datetime


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()

        self.new_movie = {
            'title': 'Avengers 12',
            'release_date': datetime.date(2025, 3, 14),
        }

        self.new_actor = {
            'name': 'Cristobal Garib',
            'gender': 'Male',
            'age': 32,
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_all_movies(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 200)

    def test_fail_get_movies(self):
        res = self.client().get('/movie')
        self.assertEqual(res.status_code, 404)

    def test_get_all_actors(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)

    def test_fail_get_actors(self):
        res = self.client().get('/actor')
        self.assertEqual(res.status_code, 404)

    def test_post_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], 'Avengers 12')

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'Cristobal Garib')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_delete_movie(self):
        res = self.client().delete('/movies/100')
        self.assertEqual(res.status_code, 404)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_delete_actor(self):
        res = self.client().delete('/actors/1000')
        self.assertEqual(res.status_code, 404)

    def test_edit_movie(self):
        res = self.client().patch('/movies/2', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_edit_movie(self):
        res = self.client().patch('/movies/10', json=self.new_movie)
        self.assertEqual(res.status_code, 404)

    def test_edit_actor(self):
        res = self.client().patch('/actors/2', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_edit_actor(self):
        res = self.client().patch('/actors/10', json=self.new_actor)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
