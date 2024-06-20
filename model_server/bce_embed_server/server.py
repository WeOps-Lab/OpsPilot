from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi import FastAPI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes, CustomUserType
from starlette.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from typing import List
from loguru import logger

app = FastAPI(
    title="bec_embed_server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info("加载BCE Embed模型......")

embedding = HuggingFaceEmbeddings(
    model_name="./models/bce-embedding-base_v1",
    encode_kwargs={
        "normalize_embeddings": True,
        "batch_size": 32,
    },
)


def func(docs: List[Document]) -> List[Document]:
    for doc in docs:
        doc.metadata['vector'] = embedding.embed_query(doc.page_content)
    return docs


runnable = RunnableLambda(func).with_types(
    input_type=List[Document], output_type=List[Document]
)


add_routes(app, runnable)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8102)
