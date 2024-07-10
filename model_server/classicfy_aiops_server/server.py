from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from runnable.anomaly_detection.abod_runnable import AbodRunnable
from runnable.anomaly_detection.iforest_runnable import IForestRunnable
from runnable.anomaly_detection.inne_runnable import InneRunnable
from runnable.anomaly_detection.knn_runnable import KnnRunnable
from runnable.anomaly_detection.kpca_runnable import KpcaRunnable
from runnable.anomaly_detection.mad_runnable import MadRunnable
from runnable.anomaly_detection.ocssvm_runnable import OcsSvmRunnable
from runnable.anomaly_detection.suod_runnable import SuodRunnable
from runnable.anomaly_detection.xgbod_runnable import XgbodRunnable
from runnable.causation.causality_runnable import CausalityRunnable
from runnable.causation.fpgrowth_runnable import FPGrowthRunnable
from runnable.logreduce.drain_runnable import DrainRunnable
from runnable.timeseries.holt_winter_runnable import HoltWinterRunnable
from runnable.timeseries.sarima_runnable import SarimaRunnable

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

add_routes(app, MadRunnable().instance(), path="/anomaly_detection/mad")
add_routes(app, AbodRunnable().instance(), path="/anomaly_detection/abod")
add_routes(app, SuodRunnable().instance(), path="/anomaly_detection/suod")
add_routes(app, IForestRunnable().instance(), path="/anomaly_detection/iforest")
add_routes(app, KnnRunnable().instance(), path="/anomaly_detection/knn")
add_routes(app, XgbodRunnable().instance(), path="/anomaly_detection/xgbod")
add_routes(app, InneRunnable().instance(), path="/anomaly_detection/inne")
add_routes(app, KpcaRunnable().instance(), path="/anomaly_detection/kpca")
add_routes(app, OcsSvmRunnable().instance(), path="/anomaly_detection/ocssvm")

add_routes(app, HoltWinterRunnable().instance(), path="/timeseries/holt_winter")
add_routes(app, SarimaRunnable().instance(), path="/timeseries/sarima")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8110)
