import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify, render_template

from src.config.config import *
from src.core import search


es_client = Elasticsearch(ES_ADD)

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello world"

@app.route('/default-recommendation', methods=['GET','POST'])
def default_recommend():
	return jsonify(search.get_default_recommendation(es_client))

@app.route('/form-search', methods=['GET', 'POST'])
def form_search():
	if request.method == 'POST':
		return jsonify(search.search_film(es_client, json.dumps(request.form['film'], ensure_ascii= False)))
	else:
		return render_template('form.html')
