import pandas as pd
from datetime import datetime


INPUT_PATH = "data/processed/viral_alerts.csv"
OUTPUT_PATH = "data/processed/slack_alerts.txt"


def build_alert_message(row):
    return f"""
🚨 ViralRadar Alert

Topic: {row['topic']}
Status: {row['viral_status']}
Spike Multiplier: {row['spike_multiplier']}x
Spike Percentage: {row['spike_percentage']}%
Recent Mentions: {row['recent_mentions']}
Expected Mentions: {row['expected_mentions']}
Average Sentiment Score: {row['avg_sentiment_score']}
Average Score: {row['avg_score']}
Average Comments: {row['avg_comments']}

Detected At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
"""


def generate_slack_alerts():
    df = pd.read_csv(INPUT_PATH)

    viral_df = df[df["viral_status"] == "VIRAL_ALERT"]

    if viral_df.empty:
        message = "No viral alerts detected at this time."
        print(message)

        with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
            file.write(message)

        return

    alert_messages = []

    for _, row in viral_df.iterrows():
        message = build_alert_message(row)
        alert_messages.append(message)
        print(message)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(alert_messages))

    print(f"Slack-style alerts saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_slack_alerts()
