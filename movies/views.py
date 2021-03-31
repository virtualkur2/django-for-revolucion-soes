# from django.shortcuts import render
from django.http import HttpResponse  # type: ignore
from django.http import JsonResponse  # type: ignore
from django.template import loader  # type: ignore
from pymongo import MongoClient  # type: ignore
import environ  # type: ignore

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

mongo_uri = env.str('MONGO_URL')


def search(request):
    params = request.GET
    title = params.get('title', '')
    client = MongoClient(mongo_uri)
    db = client.sample_mflix
    pipeline = [
        {
            "$search": {
                "index": "revolucion",
                "autocomplete": {
                    "path": "title",
                    "query": title
                }
            }
        },
        {
            "$limit": 10
        },
        {
            "$project": {
                "_id": 0,
                "title": 1
            }
        }
    ]
    result = list(db.movies.aggregate(pipeline))
    data = {'data': result}
    return JsonResponse(data)


def index(request):
    template = loader.get_template('movies/index.html')
    context = {
        'page_title': 'Movie search'
    }
    return HttpResponse(template.render(context, request))
