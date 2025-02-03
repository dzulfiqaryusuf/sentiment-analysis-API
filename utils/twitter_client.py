from twikit import Client
import time
from datetime import datetime
from random import randint
import yaml
import asyncio

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

def get_twitter_client():
    client = Client(language='en-US')
    try:
        client.load_cookies('cookies.json')
    except Exception as e:
        print(f"Failed to load cookies: {e}")
        # Handle re-authentication if needed
    return client

async def get_tweets(client, tweets=None, keyword='', start_date=None, end_date=None):
    query = f"{keyword} since:{start_date} until:{end_date}"

    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(query, product='Top')
        print(query)
    else:
        wait_time = randint(5,10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = await tweets.next()
    return tweets