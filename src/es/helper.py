from elasticsearch_dsl import Search, connections, Q
from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import SimpleQueryString

from src.es.config import ELASTIC_HOST, ELASTIC_INDEX
from src.es.document import Film

from elasticsearch.exceptions import NotFoundError

PAGE_SIZE = 20


# CONNECTION

def connect_es():
    return Elasticsearch(ELASTIC_HOST)


def create_connection_es():
    connections.create_connection(hosts=[ELASTIC_HOST])


# AGGREGATIONS

def get_aggregation(aggs, query=None):
    client = connect_es()
    s = Search(using=client, index=ELASTIC_INDEX)
    s.aggs.bucket('unique_terms', aggs)
    if query is not None:
        s.query = query

    s = s.execute()

    return {
        'total': s.hits.total,
        'buckets': s.aggregations.unique_terms.buckets
    }


# SCAN


def scan_by_query(query):
    client = connect_es()
    s = Search(using=client, index=ELASTIC_INDEX)
    s.query = query
    return get_results_from_scan(s.scan())


def simple_scan(query, fields):
    q = SimpleQueryString(query=query, fields=fields)
    return scan_by_query(q)


# SEARCH

def simple_search(query, fields, page=1):
    query = SimpleQueryString(query=query, fields=fields)
    return search_by_query({
        'query': query.to_dict()
    }, page)


def search_by_query(query, page=1):
    client = connect_es()
    query_with_page = query
    query_with_page['size'] = PAGE_SIZE
    query_with_page['from'] = PAGE_SIZE * (page - 1)
    res = client.search(index=ELASTIC_INDEX, body=query_with_page)
    return get_results_classic(res, page)


def search_by_id(_id):
    try:
        create_connection_es()
        res = Film.get(id=_id)
        return res.to_dict()
    except NotFoundError:
        return None


# CREATE

def create_doc(data):
    create_connection_es()
    doc = Film()
    for key in data:
        value = data[key]
        if value is not None and value != '':
            setattr(doc, key, value)
    doc.save()
    return doc.meta.id


# UPDATE

def update_by_id(id, data):
    client = connect_es()
    client.update(index=ELASTIC_INDEX, doc_type='doc', id=id, body={'doc': data}, retry_on_conflict=5)


# DELETE

def delete_by_id(id):
    client = connect_es()
    s = Search(using=client, index=ELASTIC_INDEX)
    s.query = Q('term', _id=id)
    return s.delete()


# HELPER

def get_results_from_scan(res):
    data_list = list()
    results = dict()

    for hit in res:
        doc = hit.to_dict()
        doc['_id'] = hit.meta.id
        data_list.append(doc)

    results['total'] = len(data_list)
    results['data'] = data_list

    return results


def get_results_classic(res, page):
    data_list = list()
    results = dict()

    for hit in res['hits']['hits']:
        doc = hit['_source']
        doc['_id'] = hit['_id']
        data_list.append(doc)

    total = res['hits']['total']

    if page * PAGE_SIZE < total:
        results['next'] = page + 1

    if page > 1:
        results['prev'] = page - 1

    results['total'] = total
    results['data'] = data_list

    return results
