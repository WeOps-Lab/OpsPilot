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


def func(doc: Document) -> List[float]:
    return embedding.embed_query(doc)


runnable = RunnableLambda(func).with_types(input_type=Document, output_type=List[float])


add_routes(app, runnable)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8102)
