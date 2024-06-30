from dotenv import load_dotenv
from fastapi import FastAPI

from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.openai_runnable import OpenAIRunnable

load_dotenv()

app = FastAPI(
    title="chat-server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(app, OpenAIRunnable().instance(), path='/openai')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8105)
