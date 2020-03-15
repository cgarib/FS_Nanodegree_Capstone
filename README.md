# Full Stack Developer Nanodegree Capstone Project

This code is the final project for the Udacity's Full Stack Developer Nanodegree. The project simulates a casting agency, that is responsible for creating movies and managing and assigning actors to those movies. I am the Executive Producer within the company and I am creating a system to simplify and streamline our process.

This project has two models: A "Movies" table that represents the movies and an "Actors" table that represents the actors. For each movie, there are many actors (1:n).

To login use the following link:

https://coffeeudacity.auth0.com/authorize?audience=coffee&response_type=token&client_id=lhYzCsDonj5QZgq2pJ9dEgEzQyPJAKf9&redirect_uri=https://fsnanoagency.herokuapp.com/

There are three roles in the API: 

1) Casting Assistant:
    - Can view actors and movies
2) Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
3) Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

The URI of the API is: https://fsnanoagency.herokuapp.com/

The endpoints are as follows:

GET '/movies' Returns all the movies including a list of all actors of the movie

GET '/actors' Returns all actors

POST '/movies' Creates a new movie

POST '/actors' Creates a new actor

DELETE '/movies/int:movie_id' Deletes movie with id = movie_id

DELETE '/actors/int:actor_id' Deletes actor with id = actor_id

PATCH '/movies/int:movie_id' Modifies movie with id = movie_id

PATCH '/actors/int:actor_id' Modifies actor with id = actor_id