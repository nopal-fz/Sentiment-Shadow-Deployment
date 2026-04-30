import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

# parents direct
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.labelling import load_lexicons, determine_sentiment

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# create documentation folder if not exists
DOC_FOLDER = "documentation"
os.makedirs(DOC_FOLDER, exist_ok=True)

# function to load data (combined old and new)
def load_data():
    df = pd.read_csv("data/processed/combined.csv")
    return df

# call function to load lexicons
positive_lexicon, negative_lexicon = load_lexicons()

# function to create label
def create_label(text):
    _, sentiment = determine_sentiment(text, positive_lexicon, negative_lexicon)
    return sentiment

# function to prepare data (create label, drop na)
def prepare_data(df):
    df = df.copy()
    df["label"] = df["text"].apply(create_label)
    df = df.dropna(subset=["label"])
    return df

# distribution of labels
def plot_label_distribution(df):
    plt.figure()
    df["label"].value_counts().plot(kind="bar")
    plt.title("Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{DOC_FOLDER}/label_distribution.png")
    plt.close()

# label distribution by period
def plot_label_by_period(df):
    plt.figure()
    sns.countplot(data=df, x="label", hue="period")
    plt.title("Label Distribution by Period")
    plt.tight_layout()
    plt.savefig(f"{DOC_FOLDER}/label_by_period.png")
    plt.close()

# text length analysis
def text_length_analysis(df):
    df["text_length"] = df["text"].apply(lambda x: len(str(x).split()))
    plt.figure()
    sns.histplot(df["text_length"], bins=50)
    plt.title("Text Length Distribution")
    plt.tight_layout()
    plt.savefig(f"{DOC_FOLDER}/text_length_distribution.png")
    plt.close()
    logging.info(f"Avg text length: {df['text_length'].mean():.2f}")

# top words
def top_words(df, n=20):
    from collections import Counter
    words = " ".join(df["text"]).split()
    counter = Counter(words)
    top = counter.most_common(n)
    words, counts = zip(*top)
    plt.figure()
    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.title("Top Words")
    plt.tight_layout()
    plt.savefig(f"{DOC_FOLDER}/top_words.png")
    plt.close()

# compare label distribution per period
def compare_periods(df):
    logging.info("Data per period:")
    logging.info(df["period"].value_counts())
    logging.info("Label per period:")
    logging.info(pd.crosstab(df["period"], df["label"]))

# main function
def main():
    logging.info("Loading data...")
    df = load_data()
    
    logging.info("Preparing data...")
    df = prepare_data(df)

    logging.info("Checking basic info...")
    logging.info(df.info())

    logging.info("Plotting label distribution...")
    plot_label_distribution(df)

    logging.info("Plotting label by period...")
    plot_label_by_period(df)

    logging.info("Analyzing text length...")
    text_length_analysis(df)

    logging.info("Top words...")
    top_words(df)

    logging.info("Comparing periods...")
    compare_periods(df)

    logging.info(f"All plots saved to {DOC_FOLDER}/ folder")

if __name__ == "__main__":
    main()