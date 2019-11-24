from elasticsearch import Elasticsearch

from src.config.config import *


def search_film(es_client, film_name):
	query = None

	if film_name is not None:
		query = {"query": {"match_phrase": {"original_title": film_name}}}
	if query is not None:
		query = {	"_source": {"includes": [ "original_title", "poster_path", "release_date" ]},
					"query": {"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
		return es_client.search(body=query, timeout='5m')


def get_default_recommendation(es_client):
	# gioi thieu phim co do noi tieng lon nhat, san xuat sau 2005 va co doanh thu > 100 tr
	query = {"query": {"bool": {"must": [
		{"range": {"popularity": {"gte": 20}}},
		{"range": {'release_date': {"gte": "2005-01-01T00:00:00"}}},
		{"range": {"budget": {"gte": "100000000"}}}
	]}}}
	query = {	"_source": {"includes": [ "original_title", "poster_path", "release_date" ]},
				"query": {"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
	return es_client.search(body=query, timeout='5m')


if __name__ == '__main__':
	es_client = Elasticsearch(ES_ADD)
	es_result = search_film(es_client, film_name="Forrest Gump")
	# es_result = get_default_recommendation(es_client)
	print(es_result)
