import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

from src.config.config import *
from src.core import search


es_client = Elasticsearch(ES_ADD)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Cho nay cua Hung
@app.route("/")
def hello():
	return "Hello world"


@app.route('/default-recommendation', methods=['GET','POST'])
def default_recommend():
	return jsonify(search.get_default_recommendation())


@app.route('/form-search', methods=['GET', 'POST'])
def form_search():
	if request.method == 'POST':
		return jsonify(search.search_film(json.dumps(request.form['film'], ensure_ascii=False)))
	else:
		return render_template('form.html')

# Cho nay cua Duc
@app.route('/test-autocomplete')
# @cross_origin()
def test_autocomplete():
	return render_template('autocomplete.html')


@app.route('/raw/<query>')
# @cross_origin()
def raw_search(query):
	items = search.real_time_search(query)
	return items


@app.route('/logs/', methods=['POST'])
# @cross_origin()
def recommend_by_logs():
	if request.method == 'POST':
		return search.log_recommend(json.loads(request.data))


@app.route('/auto/<query>')
# @cross_origin()
def autocomplete_search(query):
	items = search.autocomplete(query)
	return items
