import base64
import os
import tempfile
from typing import List

from fastapi import FastAPI
from langchain.pydantic_v1 import Field
from langchain_community.document_loaders import UnstructuredFileLoader, RecursiveUrlLoader
from langchain_community.document_loaders.parsers.pdf import PDFMinerParser
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.document_loaders import Blob
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
import requests
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import CustomUserType, add_routes, RemoteRunnable
from starlette.middleware.cors import CORSMiddleware

from embedding.remote_embeddings import RemoteEmbeddings
from loader.doc_loader import DocLoader
from loader.image_loader import ImageLoader
from loader.pdf_loader import PDFLoader
from loader.ppt_loader import PPTLoader
from loguru import logger

app = FastAPI(
    title="Chunk Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class BaseChunkRequest(CustomUserType):
    enable_recursive_chunk_parse: bool = Field(True)
    recursive_chunk_size: int = Field(128)
    recursive_chunk_overlap: int = Field(0)

    enable_semantic_chunck_parse: bool = Field(False)
    semantic_embedding_address: str = Field("http://fast-embed-server-zh.ops-pilot:8101")

    custom_metadata: dict = Field({})


class FileChunkRequest(BaseChunkRequest):
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
    file_name: str


class WebPageChunkRequest(BaseChunkRequest):
    url: str
    max_depth: int = 1


class ManualChunkRequest(BaseChunkRequest):
    content: str


def parse_manual(request: ManualChunkRequest) -> List[Document]:
    docs = [Document(request.content)]
    return parse_docs(docs, request)


def parse_webpage(request: WebPageChunkRequest) -> List[Document]:
    loader = RecursiveUrlLoader(request.url, max_depth=request.max_depth)
    web_docs = loader.load()
    transformer = BeautifulSoupTransformer()
    docs = transformer.transform_documents(web_docs)
    return parse_docs(docs, request)


def parse_docs(docs: List[Document], request: BaseChunkRequest) -> List[Document]:
    if request.enable_semantic_chunck_parse:
        semantic_embedding_model = RemoteEmbeddings(request.semantic_embedding_address)
        semantic_chunker = SemanticChunker(embeddings=semantic_embedding_model,
                                           sentence_split_regex=r'(?<=[.?!。？！])\s*')
        docs = semantic_chunker.split_documents(docs)
        logger.info(f'语义分割后的文档数：{len(docs)}')

    if request.enable_recursive_chunk_parse:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=request.recursive_chunk_size,
            chunk_overlap=request.recursive_chunk_overlap,
        )
        docs = text_splitter.split_documents(docs)
        logger.info(f'递归分割后的文档数：{len(docs)}')

    for doc in docs:
        doc.metadata.update(request.custom_metadata)
        doc.page_content = doc.page_content.replace("\n", "").replace("\r", "").replace("\t", "").strip()
        if 'source' in doc.metadata:
            del doc.metadata["source"]

    return docs


def process_file(request: FileChunkRequest) -> List[Document]:
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
            if file_type in [".pdf"]:
                loader = PDFLoader(f.name, mode="single")
            if file_type in [".jpg", ".png"]:
                loader = ImageLoader(f.name, mode="single")
            if file_type in [".doc", ".docx"]:
                loader = DocLoader(f.name, mode="single")
            else:
                loader = UnstructuredFileLoader(f.name, mode="single")

        docs = loader.load()
        docs = parse_docs(docs, request)
    return docs


add_routes(
    app,
    RunnableLambda(process_file).with_types(input_type=FileChunkRequest, output_type=List[Document]),
    path="/file_chunk",
)

add_routes(
    app,
    RunnableLambda(parse_webpage).with_types(input_type=WebPageChunkRequest, output_type=List[Document]),
    path="/webpage_chunk",
)

add_routes(
    app,
    RunnableLambda(parse_manual).with_types(input_type=ManualChunkRequest, output_type=List[Document]),
    path="/manual_chunk",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8104)
