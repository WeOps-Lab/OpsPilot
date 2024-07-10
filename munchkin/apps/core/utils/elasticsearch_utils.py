from elasticsearch import Elasticsearch

from munchkin.components.elasticsearch import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL


def get_es_client():
    return Elasticsearch(hosts=[ELASTICSEARCH_URL], http_auth=("elastic", ELASTICSEARCH_PASSWORD))
