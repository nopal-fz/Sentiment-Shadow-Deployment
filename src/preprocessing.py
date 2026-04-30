import pandas as pd
import os
import glob
import re
import logging
import requests
from io import BytesIO

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# load normalization dictionary from GitHub
def load_kamus():
    url = "https://github.com/analysisdatasentiment/kamus_kata_baku/raw/main/kamuskatabaku.xlsx"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to download normalization dictionary")

    kamus_data = pd.read_excel(BytesIO(response.content))

    kamus_dict = dict(zip(
        kamus_data['tidak_baku'],
        kamus_data['kata_baku']
    ))

    logging.info(f"Kamus loaded: {len(kamus_dict)} entries")
    return kamus_dict

# cleaning function
def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)

    # remove emoji
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text)

    # remove symbols
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # remove extra space
    text = re.sub(r"\s+", " ", text).strip()

    return text

# normalize text using kamus
def normalize_text(text, kamus):
    if not isinstance(text, str):
        return ""

    words = text.split()
    normalized_words = [kamus.get(word, word) for word in words]

    return " ".join(normalized_words)

# Function to load all CSV files from raw data
def load_all_data(raw_path="data/raw"):
    files = glob.glob(f"{raw_path}/**/*.csv", recursive=True)

    print("\nFound files:")
    for f in files:
        print(f)

    df_list = []
    for file in files:
        df = pd.read_csv(file)
        df["source_file"] = file
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)

# Preprocessing pipeline
def preprocess(df, kamus):
    df = df.copy()

    # rename
    df.rename(columns={"comment": "text"}, inplace=True)

    # simpan raw text
    df["text_raw"] = df["text"]

    # cleaning
    df["text_clean"] = df["text_raw"].apply(clean_text)

    # normalization
    df["text"] = df["text_clean"].apply(lambda x: normalize_text(x, kamus))

    # remove empty
    df = df[df["text"] != ""]

    # remove duplicate
    df = df.drop_duplicates(subset="text")

    return df

# split old vs new data based on median published date
def split_data(df, method="period"):
    if method == "period":
        return df[df["period"] == "old"], df[df["period"] == "new"]

    elif method == "median":
        df["published_at"] = pd.to_datetime(df["published_at"])
        df = df.sort_values("published_at")
        split_date = df["published_at"].median()
        return df[df["published_at"] <= split_date], df[df["published_at"] > split_date]

# main function
def main():
    logging.info("Loading kamus...")
    kamus = load_kamus()

    logging.info("Loading raw data...")
    df = load_all_data()

    logging.info("Preprocessing data...")
    df = preprocess(df, kamus)

    os.makedirs("data/processed", exist_ok=True)

    logging.info("Saving combined dataset...")
    df.to_csv("data/processed/combined.csv", index=False)

    logging.info("Splitting old vs new...")
    old_data, new_data = split_data(df, method="period")

    old_data.to_csv("data/processed/old_data.csv", index=False)
    new_data.to_csv("data/processed/new_data.csv", index=False)

    logging.info("Done!")
    logging.info(f"Total: {len(df)}")
    logging.info(f"Old: {len(old_data)} | New: {len(new_data)}")


if __name__ == "__main__":
    main()