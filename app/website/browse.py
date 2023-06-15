from flask import Blueprint, redirect, render_template
from dotenv import load_dotenv
from os import environ
import requests
import random
import pickle


load_dotenv('../.env') # for this to be working, your pwd should be inside the app directory.
api_key = environ['API_KEY']

browse = Blueprint('browse', __name__)

popular_369  = pickle.load(open('website/static/popular_369.pkl', 'rb'))[:20]


@browse.route('/', methods=['GET'])
def reroute():
    return redirect('/browse')


@browse.route('/browse', methods=['GET'])
def home():
    return render_template('placeholder_browse.html')


@browse.route('/get_browse_data', methods=['POST'])
def get_browse_html_data():
    data = []
    for id in random.sample(popular_369, 20):
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
