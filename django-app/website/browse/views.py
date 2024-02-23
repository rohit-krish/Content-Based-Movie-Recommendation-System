from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
import random
import requests
import pickle
from dotenv import load_dotenv
from os import environ

load_dotenv("website/static/.env")
api_key = environ["API_KEY"]

popular_369 = pickle.load(open("website/static/popular_369.pkl", "rb"))[:20]


@require_GET
def home(request: WSGIRequest):
    return render(
        request, "browse_placeholder.html", {"range_2": range(2), "range_4": range(4)}
    )


@require_POST
def html_data(request: WSGIRequest):
    data = []
    for id in random.sample(popular_369, 20):
        url = f"http://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US"
        resp = requests.get(url).json()
        data.append(
            {
                "id": id,
                "title": resp.get("title"),
                "year": resp.get("release_date").split("-")[0],
                "language": resp.get("original_language").capitalize(),
                "genres": [g["name"] for g in resp.get("genres")],
                "poster_path": "https://image.tmdb.org/t/p/w500"
                + resp.get("poster_path"),
            }
        )

    indexed_data = [[data[i * 4 + j] for j in range(4)] for i in range(5)]

    return render(request, "browse.html", {"indexed_data": indexed_data})
