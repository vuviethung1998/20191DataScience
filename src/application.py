from flask import Flask
from flask_cors import CORS, cross_origin

from core.search import search_film, real_time_search

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<query>')
@cross_origin()
def hello_world(query):
    items = real_time_search(query)
    return items
