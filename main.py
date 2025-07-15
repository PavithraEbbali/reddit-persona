import os
import praw
import requests
import time
import logging
from datetime import datetime
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

class RedditPersonaGenerator:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            timeout=15
        )
        self.last_api_call = 0
        self.request_delay = 1.5  # in seconds

    def _rate_limit(self):
        elapsed = time.time() - self.last_api_call
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_api_call = time.time()

    def fetch_user_data(self, username: str) -> Tuple[List[Dict], List[Dict]]:
        try:
            redditor = self.reddit.redditor(username)
            posts, comments = [], []

            logging.info(f"Fetching posts for u/{username}")
            for post in tqdm(redditor.submissions.new(limit=25), desc="Fetching posts", total=25):
                self._rate_limit()
                posts.append({
                    "type": "post",
                    "title": post.title,
                    "content": getattr(post, 'selftext', ''),
                    "created": post.created_utc,
                    "id": post.id,
                    "url": f"https://reddit.com{post.permalink}"
                })

            logging.info(f"Fetching comments for u/{username}")
            for comment in tqdm(redditor.comments.new(limit=50), desc="Fetching comments", total=50):
                self._rate_limit()
                comments.append({
                    "type": "comment",
                    "content": comment.body,
                    "created": comment.created_utc,
                    "id": comment.id,
                    "url": f"https://reddit.com{comment.permalink}"
                })

            return posts, comments

        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return [], []

    def save_raw_data(self, username: str, posts: List[Dict], comments: List[Dict]) -> str:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/{username}_raw_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Reddit Data for u/{username}\n{'='*50}\n\n")
            f.write("POSTS:\n")
            for p in posts:
                f.write(f"[{p['id']}] {p['title']}\n")
                f.write(f"URL: {p['url']}\n")
                f.write(f"Date: {datetime.fromtimestamp(p['created'])}\n")
                f.write(f"Content:\n{p['content']}\n\n")

            f.write("\nCOMMENTS:\n")
            for c in comments:
                f.write(f"[{c['id']}]\n")
                f.write(f"URL: {c['url']}\n")
                f.write(f"Date: {datetime.fromtimestamp(c['created'])}\n")
                f.write(f"Content:\n{c['content']}\n\n")

        logging.info(f"Saved raw data to {filename}")
        return filename

    def generate_local_persona(self, username: str, posts: List[Dict], comments: List[Dict]) -> str:
        from collections import Counter
        word_counter = Counter()

        for item in posts + comments:
            if isinstance(item['content'], str):
                words = item['content'].lower().split()
                for word in words:
                    if word.isalpha() and len(word) > 4:
                        word_counter[word] += 1

        top_words = word_counter.most_common(5)
        timestamps = [item['created'] for item in posts + comments if 'created' in item]
        most_active = datetime.fromtimestamp(max(timestamps)) if timestamps else "N/A"

        summary = f"""
Basic Persona Analysis for u/{username}
{'='*50}
Top Interests:
""" + "\n".join([f"- {word} (mentioned {count} times)" for word, count in top_words])

        summary += f"""

Activity Summary:
- {len(posts)} posts analyzed
- {len(comments)} comments analyzed
- Most active time: {most_active}

Note: This is a basic analysis based on word frequency.
"""
        return summary.strip()

    def generate_persona(self, username: str, posts: List[Dict], comments: List[Dict]) -> str:
        logging.info("Performing local (offline) persona analysis")
        return self.generate_local_persona(username, posts, comments)

#MAIN
if __name__ == "__main__":
    try:
        reddit_url = input("📎 Enter Reddit profile URL: ").strip()
        if reddit_url.endswith("/"):
            reddit_url = reddit_url[:-1]
        username = reddit_url.split("/")[-1]

        generator = RedditPersonaGenerator()
        posts, comments = generator.fetch_user_data(username)

        if not posts and not comments:
            print("❌ No public Reddit activity found.")
        else:
            raw_file = generator.save_raw_data(username, posts, comments)
            persona = generator.generate_persona(username, posts, comments)

            print("\n🎭 Generated Persona:")
            print(persona)
            print(f"\n📄 Raw data saved to: {raw_file}")

    except Exception as e:
        logging.error(f"❌ Script failed: {e}")
