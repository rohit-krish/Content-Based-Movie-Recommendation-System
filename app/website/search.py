from flask import Blueprint, request
import pandas as pd

search = Blueprint('search', __name__)
movies = pd.read_parquet('website/static/id_title.parquet')


def html_block_template(href, title):
    return f'<li><a class="dropdown-item" href="{href}" target="_blank">{title}</a></li>'


@search.route('/search', methods=['GET'])
def query():
    query = request.args.get('query', '')

    results_html = ''

    filtered_movies = movies[
        movies['title'].str.contains(query, case=False, na=False)
    ]

    for d in filtered_movies.values:
        results_html += html_block_template(f'detail?id={d[0]}', d[1])

    return results_html
