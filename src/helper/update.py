from elasticsearch_dsl import A

from es.helper import *

from thread_pool import ThreadPool


def add_suggestion(item):
    data = {
        'suggestion': item['original_title']
    }
    for value in item.get('characters', []):
        data['suggestion'] += ' ' + value['char_name']
    for value in item.get('directors', []):
        data['suggestion'] += ' ' + value['director_name']
    update_by_id(item['_id'], data)
    print(item['original_title'])


if __name__ == '__main__':
    q = Q('exists', field='id') & ~Q('exists', field='suggestion')
    pool = ThreadPool(40)
    pool.map(add_suggestion, scan_by_query(q)['data'])
    pool.wait_completion()
