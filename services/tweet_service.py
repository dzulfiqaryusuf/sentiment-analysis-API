from utils.twitter_client import get_twitter_client, get_tweets
from models.tweet_model import Tweet
from utils.db import SessionLocal
from twikit import TooManyRequests
from datetime import datetime
import time

def fetch_and_store_tweets(minimum_tweets=20):
    client = get_twitter_client()
    tweet_count = 0
    tweets = None
    session = SessionLocal()
    try:
        while tweet_count < minimum_tweets:
            try:
                tweets = get_tweets(client, tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
                time.sleep(max(wait_time, 0))
                continue

            if not tweets:
                print(f'{datetime.now()} - No more tweets found')
                break

            for tweet in tweets:
                if tweet_count >= minimum_tweets:
                    break
                tweet_entry = Tweet(
                    text=tweet.text,
                    created_at=tweet.created_at,
                    retweets=tweet.retweet_count,
                    likes=tweet.favorite_count
                )
                session.add(tweet_entry)
                tweet_count += 1
                print(f'Prepared INSERT for tweet {tweet_count}')

            session.commit()
            print(f'{datetime.now()} - Committed tweets. Total tweets: {tweet_count}')
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    return tweet_count
