import pandas as pd
import os
from datetime import datetime

LOG_PATH = "logs/shadow_log.csv"

def log_prediction(text, pred_v1, pred_v2):
    os.makedirs("logs", exist_ok=True)

    data = {
        "timestamp": datetime.now(),
        "text": text,
        "model_v1": pred_v1,
        "model_v2": pred_v2,
        "disagree": pred_v1 != pred_v2
    }

    df = pd.DataFrame([data])

    if os.path.exists(LOG_PATH):
        df.to_csv(LOG_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(LOG_PATH, index=False)