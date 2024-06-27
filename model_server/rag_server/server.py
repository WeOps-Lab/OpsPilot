from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.elasticsearch_index_runnable import ElasticSearchIndexRunnable
from runnable.elasticsearch_rag_runnable import ElasticSearchRagRunnable

load_dotenv()

app = FastAPI(
    title="rag_server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(app, ElasticSearchIndexRunnable().instance(), path='/elasticsearch_index')
add_routes(app, ElasticSearchRagRunnable().instance(), path='/elasticsearch_rag')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8106)
