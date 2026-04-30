import pandas as pd

# function unduh kamus positif dan negatif
def load_lexicons():
    positive_url = 'https://raw.githubusercontent.com/fajri91/InSet/master/positive.tsv'
    negative_url = 'https://raw.githubusercontent.com/fajri91/InSet/master/negative.tsv'

    positive_lexicon = set(pd.read_csv(positive_url, sep='\t', header=None)[0])
    negative_lexicon = set(pd.read_csv(negative_url, sep='\t', header=None)[0])
    
    return positive_lexicon, negative_lexicon

def determine_sentiment(text, positive_lexicon, negative_lexicon):
    if isinstance(text, str):
        positive_count = sum(1 for word in text.split() if word in positive_lexicon)
        negative_count = sum(1 for word in text.split() if word in negative_lexicon)
        sentiment_score = positive_count - negative_count
        if sentiment_score > 0:
            sentiment = 'Positif'
        elif sentiment_score < 0:
            sentiment = 'Negatif'
        else:
            sentiment = 'Netral'
        return sentiment_score, sentiment
    return 0, 'Netral'