from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.causation.causality_runnable import CausalityRunnable
from runnable.causation.fpgrowth_runnable import FPGrowthRunnable
from runnable.logreduce.drain_runnable import DrainRunnable

app = FastAPI(
    title="Classicfy Aiops Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(app, DrainRunnable().instance(), path="/logreduce/drain")
add_routes(app, CausalityRunnable().instance(), path="/causation/causality")
add_routes(app, FPGrowthRunnable().instance(), path="/causation/fpgrowth")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8110)
