from flask import Blueprint, redirect, render_template
from dotenv import load_dotenv
from os import environ
import requests
import random


load_dotenv(
    '/home/rohit/Desktop/Machine Learning/Projects/Movie-Recommendation-System/.env')
api_key = environ['API_KEY']

browse = Blueprint('browse', __name__)

popular_50 = [
    91314, 8869, 19995, 411, 102382, 296096, 671, 168259, 1858, 672, 557, 673, 674, 157336, 767, 68718, 1930, 76203, 597, 675, 585, 24428, 216015, 808, 238,
    232672, 198663, 862, 559, 1865, 14836, 8587, 22803, 38757, 2062, 106, 50014, 106646, 293660, 118340, 809, 22, 14160, 37165, 285, 99861, 425, 177572, 18785, 10198
]


@browse.route('/', methods=['GET'])
def reroute():
    return redirect('/browse')


@browse.route('/browse', methods=['GET'])
def home():
    return render_template('placeholder_browse.html')


@browse.route('/get_browse_data', methods=['POST'])
def get_browse_html_data():
    data = []
    for id in random.sample(popular_50, 20):
        url = f'http://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US'
        resp = requests.get(url).json()
        data.append({
            'id': id,
            'title': resp.get('title'),
            'year': resp.get('release_date').split('-')[0],
            'language': resp.get('original_language').capitalize(),
            'genres': [g['name'] for g in resp.get('genres')],
            'poster_path': 'https://image.tmdb.org/t/p/w500'+resp.get('poster_path')
        })

    return {'data': render_template('browse.html', data=data)}
