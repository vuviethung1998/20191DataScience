from elasticsearch_dsl import (
    connections,
    Document,
    Text,
    Date,
    Integer,
    Boolean,
    Keyword,
    Float,
    Nested
)

from src.es.config import ELASTIC_HOST, ELASTIC_INDEX


class Film(Document):
    id = Keyword(required=True)
    imdb_id = Keyword()
    original_title = Text()
    characters = Nested(properties={'char_id': Keyword(), 'char_name': Text()})
    directors = Nested(properties={'director_id': Keyword(), 'director_name': Text()})
    original_language = Keyword()
    adult = Boolean()
    belongs_to_collection = Text()
    genres = Keyword(multi=True)
    popularity = Float()
    release_date = Date()
    budget = Float()
    revenue = Float()
    runtime = Float()
    spoken_languages = Keyword(multi=True)
    poster_path = Keyword()
    vote_average = Float()
    vote_count = Integer()
    keywords = Nested(properties={'keyword': Keyword()})

    class Index:
        name = ELASTIC_INDEX


if __name__ == '__main__':
    connections.create_connection(hosts=[ELASTIC_HOST])
    # Film.init()
