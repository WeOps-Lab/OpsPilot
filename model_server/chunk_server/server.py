from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.file_chunk_runnable import FileChunkRunnable
from runnable.manual_chunk_runnable import ManualChunkRunnable
from runnable.web_page_chunk_runnable import WebPageChunkRunnable

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

add_routes(app, FileChunkRunnable().instance(), path="/file_chunk")

add_routes(app, WebPageChunkRunnable().instance(), path="/webpage_chunk")

add_routes(app, ManualChunkRunnable().instance(), path="/manual_chunk")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8104)
