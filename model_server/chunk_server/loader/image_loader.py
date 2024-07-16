import base64

import requests
from langchain_core.documents import Document
from langserve import RemoteRunnable

from user_types.file_chunk_request import FileChunkRequest


class ImageLoader:
    def __init__(self, path, chunk_request: FileChunkRequest):
        self.path = path
        self.chunk_request = chunk_request

    def load(self):
        docs = []
        with open(self.path, "rb") as file:
            file_remote = RemoteRunnable(self.chunk_request.ocr_provider_address)
            content = file_remote.invoke({
                "file": base64.b64encode(file.read()).decode('utf-8'),
            })
            docs.append(Document(content, metadata={"format": "image"}))
        return docs
