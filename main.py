from fastapi import FastAPI
import joblib
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from typing import List
from pydantic import BaseModel
from src.inference import predict_lr
from src.psutil_system_metrics import PsutilSystemMetrics
from src.request_metrics import RequestMetrics
from src.logger import Logger


logger = Logger("uvicorn")
app = FastAPI()
system_metrics = PsutilSystemMetrics()
request_metrics = RequestMetrics()
model = joblib.load("src/linear_regression_model.pkl")


def update_system_metrics():
    system_metrics.update()


@app.on_event("startup")
def startup_event():
    update_system_metrics()


@app.middleware("http")
async def record_request_time(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    request_metrics.record_latency(latency)
    return response


@app.get("/metrics")
def metrics():
    update_system_metrics()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


class Features(BaseModel):
    features: List[float]


@app.post("/predict/")
async def predict(features: Features):
    prediction = predict_lr(model, features.features)

    logger.info(f"Received request: features={features.features}, result={prediction}")
    return {"prediction": prediction}
