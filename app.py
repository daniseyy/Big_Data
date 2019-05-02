from flask import Blueprint

main = Blueprint('main', __name__)

import json
from engine import RecommendationEngine

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request


@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    """"Untuk menampilkan sejumlah <count> rekomendasi film ke user <user_id>"""
    logger.debug("User %s TOP ratings requested", user_id)
    top_rated = recommendation_engine.get_top_ratings(user_id, count)
    return json.dumps(top_rated)


@main.route("/artist/<int:artist>/recommend/<int:count>", methods=["GET"])
def movie_recommending(artist, count):
    """"Untuk menampilkan film <movie_id> terbaik direkomendasikan ke sejumlah <count> user"""
    logger.debug("MovieId %s TOP user recommending", movie_id)
    top_rated = recommendation_engine.get_top_artist_recommend(movie_id, count)
    return json.dumps(top_rated)



@main.route("/<int:user_id>/history", methods=["GET"])
def ratings_history(user_id):
    """"Untuk melihat riwayat pemberian rating oleh user <user_id>"""
    logger.debug("History for user %s is requested", user_id)
    user_history = recommendation_engine.get_history(user_id)
    return json.dumps(user_history)

@main.route("/<int:user_id>/giverating", methods=["POST"])
def add_ratings(user_id):
    """"Untuk submit <user_id> memberikan rating untuk film X"""
    # get the ratings from the Flask POST request object
    movieId_fetched = int(request.form.get('movieId'))
    ratings_fetched = float(request.form.get('ratingGiven'))
    # print(movieId_fetched)
    # print(ratings_fetched)
    # add them to the model using then engine API
    new_rating = recommendation_engine.add_ratings(user_id, movieId_fetched, ratings_fetched)
    # ratings = ratings.toJSON()
    return json.dumps(new_rating)


def create_app(spark_session, dataset_path):
    global recommendation_engine

    recommendation_engine = RecommendationEngine(spark_session, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app
