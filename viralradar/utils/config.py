import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ViralRadar/1.0")

SUBREDDITS = os.getenv(
    "SUBREDDITS",
    "technology,artificial,MachineLearning,worldnews"
).split(",")
