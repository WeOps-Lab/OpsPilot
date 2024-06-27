from langserve import CustomUserType


class ElasticSearchRequest(CustomUserType):
    elasticsearch_url: str = "http://elasticsearch.ops-pilot:9200"
    elasticsearch_password: str
    embed_model_address: str
