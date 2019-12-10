import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q

from src.config.config import *
from src.helper.es.helper import search_by_query, get_suggestion

from src.model.als_recommend import recommend


def get_client():
	return Elasticsearch(ES_ADD)


def search_film(film_name):
	es_client = get_client()
	query = None

	if film_name is not None:
		query = {"query": {"match_phrase": {"original_title": film_name}}}
	if query is not None:
		query = {	"_source": {"includes": [ "original_title", "poster_path", "release_date" ]},
					"query": {"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
		return es_client.search(body=query, timeout='5m')


def get_default_recommendation():
	es_client = get_client()
	# gioi thieu phim co do noi tieng lon nhat, san xuat sau 2005 va co doanh thu > 100 tr
	query = {"query": {"bool": {"must": [
		{"range": {"popularity": {"gte": 20}}},
		{"range": {'release_date': {"gte": "2005-01-01T00:00:00"}}},
		{"range": {"budget": {"gte": "100000000"}}}
	]}}}
	query = {	"_source": {"includes": [ "original_title", "poster_path", "release_date" ]},
				"query": {"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
	return es_client.search(body=query, timeout='5m')


def search_director(es_client, director_name):
	query = None

	if director_name is not None:
		query = {"query": {}}


# Cho nay cua Duc
def real_time_search(query):
	q = Q('match', original_title=query) \
		| Q('match', directors__director_name=query) \
		| Q('match', characters__char_name=query)
	return search_by_query({'query': q.to_dict()})


def autocomplete(text):
	return get_suggestion(text, 'suggestion')


def log_recommend(logs):
	results = list(recommend(logs))
	q = None
	for film_id in results:
		if q is None:
			q = Q('term', id=int(film_id))
		else:
			q = q | Q('term', id=int(film_id))
	return search_by_query({'query': q.to_dict()})


if __name__ == '__main__':
	es_client = Elasticsearch(ES_ADD)
	es_result = search_film(es_client, film_name="Forrest Gump")
	# es_result = get_default_recommendation(es_client)
	print(es_result)
