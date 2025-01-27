from transformers import pipeline
from models.tweet_model import Tweet
from utils.db import SessionLocal

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

def analyze_sentiment():
    session = SessionLocal()
    try:
        tweets = session.query(Tweet).order_by(Tweet.created_at.desc()).limit(100).all()
        sentiments = []
        for tweet in tweets:
            result = sentiment_pipeline(tweet.text[:512])[0]  # Truncate to 512 tokens
            sentiments.append({
                'tweet_id': tweet.id,
                'username': tweet.username,
                'text': tweet.text,
                'sentiment': result['label'],
                'score': result['score']
            })
        return sentiments
    finally:
        session.close()
