import base64
import os
import tempfile
from typing import List

import requests
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from loader.doc_loader import DocLoader
from loader.image_loader import ImageLoader
from loader.pdf_loader import PDFLoader
from loader.ppt_loader import PPTLoader
from runnable.base_chunk_runnable import BaseChunkRunnable
from user_types.file_chunk_request import FileChunkRequest


class FileChunkRunnable(BaseChunkRunnable):
    def __init__(self):
        pass

    def parse(self, request: FileChunkRequest) -> List[Document]:
        content = base64.b64decode(request.file.encode("utf-8"))
        file_name, file_type = os.path.splitext(request.file_name)
        pure_filename = file_name.split("/")[-1]

        with tempfile.NamedTemporaryFile(delete=False) as f:
            if file_type in [".md"]:
                response = requests.post(
                    'http://pandoc-server.ops-pilot:8103/convert',
                    data={'output': 'pdf'},
                    files={'file': (pure_filename + file_type, content)}
                )
                f.write(response.content)

                loader = PDFLoader(f.name, mode="single")
            else:
                f.write(content)

                if file_type in [".ppt", ".pptx"]:
                    loader = PPTLoader(f.name, mode="single")
                elif file_type in [".pdf"]:
                    loader = PDFLoader(f.name, mode="single")
                elif file_type in [".jpg", ".png"]:
                    loader = ImageLoader(f.name, mode="single")
                elif file_type in [".doc", ".docx"]:
                    loader = DocLoader(f.name, mode="single")
                else:
                    loader = UnstructuredFileLoader(f.name, mode="single")

            docs = loader.load()
            docs = self.parse_docs(docs, request)
        return docs

    def instance(self):
        return RunnableLambda(self.parse).with_types(input_type=FileChunkRequest, output_type=List[Document])
