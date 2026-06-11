import pandas as pd


INPUT_PATH = "data/processed/enriched_posts.csv"
OUTPUT_PATH = "data/processed/viral_alerts.csv"

RECENT_WINDOW_MINUTES = 30
BASELINE_WINDOW_MINUTES = 150
SPIKE_THRESHOLD = 1.2


def detect_spikes():
    df = pd.read_csv(INPUT_PATH)

    df["created_utc"] = pd.to_datetime(df["created_utc"], utc=True)

    latest_time = df["created_utc"].max()
    recent_start = latest_time - pd.Timedelta(minutes=RECENT_WINDOW_MINUTES)
    baseline_start = latest_time - pd.Timedelta(minutes=RECENT_WINDOW_MINUTES + BASELINE_WINDOW_MINUTES)

    recent_df = df[df["created_utc"] >= recent_start]

    baseline_df = df[
        (df["created_utc"] >= baseline_start) &
        (df["created_utc"] < recent_start)
    ]

    recent_counts = recent_df.groupby("topic").size().reset_index(name="recent_mentions")
    baseline_counts = baseline_df.groupby("topic").size().reset_index(name="baseline_mentions")

    alerts = recent_counts.merge(baseline_counts, on="topic", how="left")
    alerts["baseline_mentions"] = alerts["baseline_mentions"].fillna(0)

    # Convert baseline count into expected mentions for a 30-minute window
    alerts["expected_mentions"] = alerts["baseline_mentions"] / (BASELINE_WINDOW_MINUTES / RECENT_WINDOW_MINUTES)

    # Avoid division by zero
    alerts["expected_mentions"] = alerts["expected_mentions"].replace(0, 0.5)

    alerts["spike_multiplier"] = alerts["recent_mentions"] / alerts["expected_mentions"]
    alerts["spike_percentage"] = ((alerts["spike_multiplier"] - 1) * 100).round(2)

    sentiment_summary = (
        recent_df.groupby("topic")["sentiment_score"]
        .mean()
        .reset_index(name="avg_sentiment_score")
    )

    engagement_summary = (
        recent_df.groupby("topic")[["score", "num_comments"]]
        .mean()
        .reset_index()
        .rename(columns={
            "score": "avg_score",
            "num_comments": "avg_comments"
        })
    )

    alerts = alerts.merge(sentiment_summary, on="topic", how="left")
    alerts = alerts.merge(engagement_summary, on="topic", how="left")

    alerts["viral_status"] = alerts["spike_multiplier"].apply(
        lambda x: "VIRAL_ALERT" if x >= SPIKE_THRESHOLD else "normal"
    )

    alerts = alerts.sort_values(by="spike_multiplier", ascending=False)

    alerts.to_csv(OUTPUT_PATH, index=False)

    print("Spike detection completed")
    print(f"Saved alerts to {OUTPUT_PATH}")
    print(alerts)


if __name__ == "__main__":
    detect_spikes()
