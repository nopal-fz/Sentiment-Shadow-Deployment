import pandas as pd
import os
import joblib
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# parents direct
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.labelling import load_lexicons, determine_sentiment

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# call function to load lexicons
positive_lexicon, negative_lexicon = load_lexicons()

# function to create label
def create_label(text):
    _, sentiment = determine_sentiment(text, positive_lexicon, negative_lexicon)
    return sentiment

# function to load data
def load_data():
    old_df = pd.read_csv("data/processed/old_data.csv")
    new_df = pd.read_csv("data/processed/new_data.csv")

    return old_df, new_df

# function to prepare data (create label, drop na)
def prepare_data(df):
    df = df.copy()

    df["label"] = df["text"].apply(create_label)

    # drop yang gak ada label
    df = df.dropna(subset=["label"])

    return df

# function to evaluate model
def evaluate(model, vectorizer, X, y, name="Model"):
    X_vec = vectorizer.transform(X)
    y_pred = model.predict(X_vec)

    logging.info(f"\n{name} Evaluation:\n{classification_report(y, y_pred)}")

# main function
def main():
    logging.info("Loading data...")
    old_df, new_df = load_data()

    logging.info("Preparing old data...")
    old_df = prepare_data(old_df)

    logging.info("Preparing new data...")
    new_df = prepare_data(new_df)

    # fit vectorizer on old data only
    logging.info("Fitting vectorizer on old data...")

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_old = vectorizer.fit_transform(old_df["text"])
    y_old = old_df["label"]

    # train model on old data
    logging.info("Training Model v1 (old data)...")

    model_v1 = LogisticRegression(max_iter=1000)
    model_v1.fit(X_old, y_old)

    evaluate(model_v1, vectorizer, old_df["text"], old_df["label"], "Model v1")

    # train model on new data but same vectorizer (no refit)
    logging.info("Training Model v2 (new data)...")

    X_new = vectorizer.transform(new_df["text"])
    y_new = new_df["label"]

    model_v2 = LogisticRegression(max_iter=1000)
    model_v2.fit(X_new, y_new)

    evaluate(model_v2, vectorizer, new_df["text"], new_df["label"], "Model v2")

    # save models and vectorizer
    os.makedirs("models", exist_ok=True)

    joblib.dump(model_v1, "models/model_v1.pkl")
    joblib.dump(model_v2, "models/model_v2.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")

    logging.info("Models saved successfully!")

if __name__ == "__main__":
    main()