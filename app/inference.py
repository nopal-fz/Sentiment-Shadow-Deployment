import joblib

# load models & vectorizer sekali di awal
model_v1 = joblib.load("models/model_v1.pkl")
model_v2 = joblib.load("models/model_v2.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def predict(text):
    X = vectorizer.transform([text])

    pred_v1 = model_v1.predict(X)[0]
    pred_v2 = model_v2.predict(X)[0]

    return pred_v1, pred_v2