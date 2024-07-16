from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.azure_ocr_runnable import AzureOcrRunnable
from runnable.paddle_ocr_runnable import PaddleOcrRunnable

app = FastAPI(
    title="OCR Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(app, PaddleOcrRunnable().instance(), path="/paddle_ocr")
add_routes(app, AzureOcrRunnable().instance(), path='/azure_ocr')
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8109)
