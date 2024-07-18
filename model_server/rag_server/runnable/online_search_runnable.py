from itertools import islice
from typing import List

import urllib3
from loguru import logger
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from user_types.online_search_request import OnlineSearchRequest
from duckduckgo_search import DDGS


class OnlineSearchRagRunnable:
    def __init__(self):
        pass

    def execute(self, req: OnlineSearchRequest) -> List[Document]:
        doc_list = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(req.query, backend="lite")
            for r in islice(ddgs_gen, 10):
                doc_list.append(Document(r["body"], metadata={"url": r["href"], "title": r['title']}))
        return doc_list

    def instance(self):
        return RunnableLambda(self.execute).with_types(
            input_type=OnlineSearchRequest,
            output_type=List[Document])
