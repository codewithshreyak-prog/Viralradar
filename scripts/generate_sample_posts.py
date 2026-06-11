import pandas as pd
from datetime import datetime, timedelta, timezone
import random

topics = [
    "OpenAI agents",
    "AI video tools",
    "Tesla robotaxi",
    "Apple Vision Pro",
    "NVIDIA chips",
    "Layoffs in tech",
    "New iPhone leak",
    "AI jobs",
    "Reddit outage",
    "Cybersecurity breach"
]

subreddits = ["technology", "artificial", "MachineLearning", "worldnews"]

rows = []
now = datetime.now(timezone.utc)

for i in range(250):
    topic = random.choice(topics)

    # Make some topics appear more often recently to simulate viral spike
    if i > 180:
        topic = random.choice(["OpenAI agents", "Tesla robotaxi", "AI video tools"])

    created_time = now - timedelta(minutes=random.randint(0, 180))

    rows.append({
        "post_id": f"demo_{i}",
        "title": f"{topic} is gaining attention online with users discussing major updates",
        "topic": topic,
        "subreddit": random.choice(subreddits),
        "score": random.randint(10, 5000),
        "num_comments": random.randint(1, 900),
        "upvote_ratio": round(random.uniform(0.65, 0.99), 2),
        "created_utc": created_time.isoformat(),
        "url": "https://reddit.com/demo"
    })

df = pd.DataFrame(rows)
df.to_csv("data/raw/reddit_posts.csv", index=False)

print("Generated sample Reddit-style data")
print("Saved to data/raw/reddit_posts.csv")
print(df.head())
