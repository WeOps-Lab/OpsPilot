import requests
from langchain_core.documents import Document

from user_types.file_chunk_request import FileChunkRequest


class ImageLoader:
    def __init__(self, path, chunk_request: FileChunkRequest):
        self.path = path
        self.chunk_request = chunk_request

    def load(self):
        docs = []
        with open(self.path, "rb") as file:
            response = requests.post(self.chunk_request.ocr_provider_address, files={"file": file})
            response.raise_for_status()
            content = response.json()['text']
            docs.append(Document(content))
        return docs
