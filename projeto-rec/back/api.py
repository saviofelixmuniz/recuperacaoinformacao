from flask import Flask
from flask import json
from flask import request
from flask import Response
from flask_cors import CORS
import os

import recommender

app = Flask(__name__)
CORS(app)


@app.route("/api/recommendation", methods=['POST'])
def recommend():
    watched_movies = request.json
    data = recommender.recommend(watched_movies["movie_ids"])[0:20]

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/api/movies")
def get_movies():
    js = json.dumps(recommender.read_all_movies())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9090))
    app.run(port=port)
