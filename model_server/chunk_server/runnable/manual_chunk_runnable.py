from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from runnable.base_chunk_runnable import BaseChunkRunnable
from user_types.manual_chunk_request import ManualChunkRequest


class ManualChunkRunnable(BaseChunkRunnable):
    def __init__(self):
        pass

    def parse(self, request: ManualChunkRequest) -> List[Document]:
        docs = [Document(request.content)]
        return self.parse_docs(docs, request)

    def instance(self):
        return RunnableLambda(self.parse).with_types(input_type=ManualChunkRequest, output_type=List[Document])
