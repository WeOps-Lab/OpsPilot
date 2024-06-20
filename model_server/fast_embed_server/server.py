import os
from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from fastapi import FastAPI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes, CustomUserType
from starlette.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from typing import List
from loguru import logger

load_dotenv()

app = FastAPI(
    title="fast_embed_server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


model_name = os.getenv("MODEL_NAME", "BAAI/bge-small-zh-v1.5")
logger.info(f"Using model: {model_name}")

embedding = FastEmbedEmbeddings(model_name=model_name, cache_dir="models")


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

    uvicorn.run(app, host="0.0.0.0", port=8101)
