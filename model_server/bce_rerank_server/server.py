from BCEmbedding.tools.langchain import BCERerank
from fastapi import FastAPI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes, CustomUserType
from starlette.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from typing import List
from loguru import logger

app = FastAPI(
    title="bce_rerank_server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info("加载BCE Reranker模型......")

reranker_args = {
    "model": './models/bce-reranker-base_v1',
}
reranker = BCERerank(**reranker_args)


class ReRankerEntity(CustomUserType):
    docs: List[Document]
    query: str
    top_n: int = 10


def func(entity: ReRankerEntity) -> List[Document]:
    reranker.top_n = entity.top_n
    compressed_data = reranker.compress_documents(entity.docs, entity.query)
    return compressed_data


runnable = RunnableLambda(func).with_types(
    input_type=ReRankerEntity, output_type=List[Document]
)

add_routes(app, runnable)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8100)
