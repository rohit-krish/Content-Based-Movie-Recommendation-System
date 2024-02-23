from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
import pandas as pd

movies = pd.read_parquet("website/static/id_title.parquet")


def html_block_template(href, title):
    return (
        f'<li><a class="dropdown-item" href="{href}" target="_blank">{title}</a></li>'
    )


def search(request: WSGIRequest):
    query = request.GET.get("query", "")

    results_html = ""

    filtered_movies = movies[movies["title"].str.contains(query, case=False, na=False)]

    for d in filtered_movies.values:
        results_html += html_block_template(f"/detail?id={d[0]}", d[1])

    return HttpResponse(results_html)
