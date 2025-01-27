from twikit import Client
import time
from datetime import datetime
from random import randint
import yaml
query = 'mytelkomsel'
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

def get_tweets(client, tweets=None):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = client.search_tweet(query, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()
    return tweets
