from flask import Blueprint, render_template, request
from dotenv import load_dotenv
from os import environ
import requests
import pandas as pd

load_dotenv()
api_key = environ['API_KEY']

movie_ids = pd.read_parquet('website/static/id_title.parquet', columns=['id'])
similarity_df = pd.read_parquet('website/static/similarity_df.parquet')


def recommend(id, limit=8):
    movie_index = movie_ids[movie_ids['id'] == int(id)].index[0]
    distances = similarity_df.iloc[movie_index].values
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:limit+1]

    return [movie_ids.iloc[m[0]].id for m in movies_list]


def get_data(movie_id):
    meta_url = f'http://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    meta_resp = requests.get(meta_url).json()
    data = {
        'poster_path': 'https://image.tmdb.org/t/p/w500'+meta_resp.get('poster_path'),
        'title': meta_resp.get('title'),
        'release_date': meta_resp.get('release_date'),
        'genres': [g['name'] for g in meta_resp.get('genres')],
        'popularity': f"{float(meta_resp.get('popularity')):.1f}",
        'overview': meta_resp.get('overview')
    }

    credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US'
    credits_resp = requests.get(credits_url).json()

    data['directors'] = [
        c['name']
        for c in credits_resp.get('crew') if c['job'] == 'Director'
    ]

    actors = sorted(
        credits_resp.get('cast'), key=lambda x: x['popularity']
    )[::-1][:6]

    data['cast'] = [
        {'name': c['name'], 'profile_path': 'https://image.tmdb.org/t/p/w500'+c['profile_path']} for c in actors
    ]

    # print('meta_data loaded', '***')

    recommendations = recommend(movie_id)
    # print('got recommendations', '***')

    data['recommendation_data'] = []

    for id in recommendations:
        recom_url = f'http://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US'
        recom_resp = requests.get(recom_url).json()

        data['recommendation_data'].append({
            'id': id,
            'title': recom_resp.get('title'),
            'poster_path': 'https://image.tmdb.org/t/p/w500'+recom_resp.get('poster_path'),
            'year': recom_resp.get('release_date').split('-')[0],
            'language': recom_resp.get('original_language').capitalize(),
            'genres': [g['name'] for g in recom_resp.get('genres')]
        })

    return data


detail = Blueprint('detail', __name__)


@detail.route('/detail', methods=['GET'])
def home():
    return render_template('placeholder_detail.html', id=request.args.get('id'))


@detail.route('/get_detail_data', methods=['GET'])
def get_detail_html_data():
    data = get_data(request.args.get('id'))
    # data = pickle.load(open('website/static/sample_detail_data.pkl', 'rb'))

    return {'data': render_template('detail.html', data=data)}
