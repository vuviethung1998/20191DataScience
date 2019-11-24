from flask import Flask
from flask_cors import CORS, cross_origin

from core.search import real_time_search, autocomplete

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<query>')
@cross_origin()
def raw_search(query):
    items = real_time_search(query)
    return items

@app.route('/auto/<query>')
@cross_origin()
def autocomplete_search(query):
    items = autocomplete(query)
    return items
