import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


INPUT_PATH = "data/raw/reddit_posts.csv"
OUTPUT_PATH = "data/processed/enriched_posts.csv"


def classify_vader_sentiment(compound_score):
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"


def run_vader_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()

    sentiment_scores = []
    sentiment_labels = []
    sentiment_model = []

    for title in df["title"]:
        score = analyzer.polarity_scores(str(title))
        compound = score["compound"]

        sentiment_scores.append(compound)
        sentiment_labels.append(classify_vader_sentiment(compound))
        sentiment_model.append("VADER")

    df["sentiment_score"] = sentiment_scores
    df["sentiment"] = sentiment_labels
    df["sentiment_model"] = sentiment_model

    return df


def run_huggingface_sentiment(df):
    from transformers import pipeline

    classifier = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    )

    sentiment_scores = []
    sentiment_labels = []
    sentiment_model = []

    for title in df["title"]:
        result = classifier(str(title), truncation=True)[0]

        label = result["label"].lower()
        score = float(result["score"])

        if "positive" in label:
            normalized_label = "positive"
            normalized_score = score
        elif "negative" in label:
            normalized_label = "negative"
            normalized_score = -score
        else:
            normalized_label = "neutral"
            normalized_score = 0.0

        sentiment_scores.append(round(normalized_score, 4))
        sentiment_labels.append(normalized_label)
        sentiment_model.append("HuggingFace")

    df["sentiment_score"] = sentiment_scores
    df["sentiment"] = sentiment_labels
    df["sentiment_model"] = sentiment_model

    return df


def analyze_sentiment():
    df = pd.read_csv(INPUT_PATH)

    try:
        print("Running Hugging Face sentiment analysis...")
        df = run_huggingface_sentiment(df)
    except Exception as error:
        print("Hugging Face sentiment failed. Falling back to VADER.")
        print(f"Reason: {error}")
        df = run_vader_sentiment(df)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Sentiment analysis completed")
    print(f"Saved enriched data to {OUTPUT_PATH}")
    print(df[["title", "topic", "sentiment", "sentiment_score", "sentiment_model"]].head())


if __name__ == "__main__":
    analyze_sentiment()