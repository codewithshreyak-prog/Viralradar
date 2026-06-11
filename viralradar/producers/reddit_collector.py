import praw
import pandas as pd
from datetime import datetime, timezone
from viralradar.utils.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDITS,
)


def create_reddit_client():
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError(
            "Missing Reddit API keys. Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to your .env file."
        )

    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )


def collect_hot_posts(limit_per_subreddit=10):
    reddit = create_reddit_client()
    posts = []

    for subreddit_name in SUBREDDITS:
        subreddit_name = subreddit_name.strip()
        print(f"Collecting posts from r/{subreddit_name}...")

        subreddit = reddit.subreddit(subreddit_name)

        for post in subreddit.hot(limit=limit_per_subreddit):
            posts.append(
                {
                    "post_id": post.id,
                    "title": post.title,
                    "subreddit": subreddit_name,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "upvote_ratio": post.upvote_ratio,
                    "created_utc": datetime.fromtimestamp(
                        post.created_utc, tz=timezone.utc
                    ).isoformat(),
                    "url": post.url,
                }
            )

    return posts


def save_posts_to_csv(posts, output_path="data/raw/reddit_posts.csv"):
    df = pd.DataFrame(posts)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} posts to {output_path}")


if __name__ == "__main__":
    posts = collect_hot_posts(limit_per_subreddit=10)
    save_posts_to_csv(posts)
