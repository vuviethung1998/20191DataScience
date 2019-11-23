from elasticsearch import Elasticsearch

from src.config.config import *
from src.es.helper import simple_search


def get_client():
	return Elasticsearch(ES_ADD)


def search_film(film_name):
	es_client = get_client()
	query = None

	if film_name is not None:
		query = {"query": {"match_phrase": {"original_title": film_name}}}
	if query is not None:
		query = {"query": {
			"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
		return es_client.search(body=query, timeout='5m')


def real_time_search(query):
	fields = ['original_title', 'directors__director_name', 'characters__char_name']
	return simple_search(query, fields)


def get_default_recommendation():
	es_client = get_client()
	# gioi thieu phim co do noi tieng lon nhat, san xuat sau 2005 va co doanh thu > 100 tr
	query = {"query": {"bool": {"must": [
		{"range": {"popularity": {"gte": 20}}},
		{"range": {'release_date': {"gte": "2005-01-01T00:00:00"}}},
		{"range": {"budget": {"gte": "100000000"}}}
	]}}}
	query = {"query": {
		"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
	return es_client.search(body=query, timeout='5m')


def search_director(es_client, director_name):
	query = None

	if director_name is not None:
		query = {"query": {}}
