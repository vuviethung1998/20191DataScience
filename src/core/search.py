from elasticsearch import Elasticsearch

from src.config.config import *


def search_film(es_client, film_name):
	query = None

	if film_name is not None:
		query = {"query": {"match_phrase": {"original_title": film_name}}}
	if query is not None:
		query = {"query": {
			"function_score": {"query": query['query'], "script_score": {"script": "_score"}}}}
		return es_client.search(body=query, timeout='5m')


if __name__ == '__main__':
	es_client = Elasticsearch(ES_ADD)
	es_result = search_film(es_client, film_name="Batman")
	print(es_result)
