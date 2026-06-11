import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


INPUT_PATH = "data/raw/reddit_posts.csv"
OUTPUT_PATH = "data/processed/enriched_posts.csv"


def classify_sentiment(compound_score):
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"


def analyze_sentiment():
    df = pd.read_csv(INPUT_PATH)

    analyzer = SentimentIntensityAnalyzer()

    sentiment_scores = []
    sentiment_labels = []

    for title in df["title"]:
        score = analyzer.polarity_scores(str(title))
        compound = score["compound"]

        sentiment_scores.append(compound)
        sentiment_labels.append(classify_sentiment(compound))

    df["sentiment_score"] = sentiment_scores
    df["sentiment"] = sentiment_labels

    df.to_csv(OUTPUT_PATH, index=False)

    print("Sentiment analysis completed")
    print(f"Saved enriched data to {OUTPUT_PATH}")
    print(df[["title", "topic", "sentiment", "sentiment_score"]].head())


if __name__ == "__main__":
    analyze_sentiment()
