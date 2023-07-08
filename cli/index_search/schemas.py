from jieba.analyse import ChineseAnalyzer
from whoosh.fields import SchemaClass, TEXT


class DocSchema(SchemaClass):
    content = TEXT(stored=True, analyzer=ChineseAnalyzer())
