import os.path

from jieba.analyse import ChineseAnalyzer
from tqdm import tqdm
from whoosh import qparser
from whoosh.fields import SchemaClass, TEXT
from whoosh.index import open_dir, create_in
from whoosh.qparser import QueryParser

from actions import server_settings


class DocSchema(SchemaClass):
    content = TEXT(stored=True, analyzer=ChineseAnalyzer())


class Searcher:
    def __init__(self):
        if os.path.exists(server_settings.indexer_db_path):
            self.ix = open_dir(server_settings.indexer_db_path, indexname='doc_index')
        else:
            schema = DocSchema()
            os.mkdir(server_settings.indexer_db_path)
            self.ix = create_in(server_settings.indexer_db_path, schema, indexname='doc_index')

    def format_prompt(self, prompt_template, query):
        if '{index_context}' in prompt_template:
            index_context = ''
            with self.ix.searcher() as searcher:
                search_query = QueryParser("content", self.ix.schema, group=qparser.OrGroup).parse(query)
                query_result = searcher.search(search_query, limit=2)
                if len(query_result) > 0:
                    for result in query_result:
                        index_context += result['content'] + '\n'

            prompt_template = prompt_template.replace('{index_context}', index_context)
        return prompt_template

    def index_knowledge(self, knowledge_contents):
        writer = self.ix.writer()
        for content in tqdm(knowledge_contents, desc='索引知识文件'):
            writer.add_document(content=content)
        writer.commit()
