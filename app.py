import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/": {"origins": "*"}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Welcome to the agency!'

    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
        formated_movies = [movie.format() for movie in movies]
        for movie in formated_movies:
            movie['actors'] = [actor.format() for actor in movie['actors']]
        return jsonify(formated_movies), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        formated_actors = [actor.format() for actor in actors]
        return jsonify(formated_actors), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_new_movie(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
        except Exception:
            abort(400)

        return jsonify({
            'success': True,
            'new_movie': new_movie.format()
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_new_actor(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        try:
            new_actor = Actor(name=name, age=age, gender=gender,
                              movie_id=movie_id)
            new_actor.insert()
        except Exception:
            abort(400)

        return jsonify({
            'success': True,
            'new_actor': new_actor.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        if not movie_id:
            abort(422)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            "success": True,
            'delete': movie_id
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        if not actor_id:
            abort(422)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            "success": True,
            'delete': actor_id
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, actor_id):

        body = request.get_json()
        if body is None:
            abort(400)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.movie_id = movie_id
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, movie_id):

        body = request.get_json()
        if body is None:
            abort(400)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        movie.title = title
        movie.release_date = release_date
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        })

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
