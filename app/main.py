from fastapi import FastAPI
from pydantic import BaseModel

from app.inference import predict
from app.logger import log_prediction

app = FastAPI(title="Shadow Deployment API")

class Request(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Shadow Deployment API Running"}

@app.post("/predict")
def predict_endpoint(req: Request):
    text = req.text

    pred_v1, pred_v2 = predict(text)

    # log shadow comparison
    log_prediction(text, pred_v1, pred_v2)

    return {
        "prediction": pred_v1, # production output
        "shadow_prediction": pred_v2,
        "is_different": pred_v1 != pred_v2
    }