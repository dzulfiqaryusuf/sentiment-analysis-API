from flask import Blueprint, jsonify,request
from services.sentiment_service import get_sentiment_from_db
from collections import Counter
from models.tweet_model import Tweet
from utils.db import SessionLocal
import requests
from datetime import datetime
import pytz
from pprint import pprint

FETCH_TWEETS_API_URL = 'http://127.0.0.1:5000/api/fetch_tweets'

timezone = pytz.timezone('Asia/Jakarta')
now = datetime.now(timezone)
sentiment_bp = Blueprint('sentiments', __name__)
session = SessionLocal()

@sentiment_bp.route('/analyze_sentiment', methods=['POST'])
def sentiment():
    try:
        min_tweets = request.json.get('min_tweets', 200)
        keyword = request.json.get('keyword')
        start_date = request.json.get('start_date',datetime(now.year, now.month, 1, 0, 0, 0, 0).replace(tzinfo=timezone))
        end_date = request.json.get('end_date', datetime.now(timezone))
        print(f'Start date: {start_date}, End date: {end_date}')
        print(f'Keyword: {keyword}')
        
        existing_tweets = session.query(Tweet).filter(
            Tweet.text.ilike(f"%{keyword}%"), 
            Tweet.created_at >= start_date,
            Tweet.created_at <= end_date
        ).all()
        print(len(existing_tweets))
        print(len(existing_tweets) >= 50)

        # If tweets are already in the database, skip fetching
        if len(existing_tweets) >= 50:
            print(f"Found {len(existing_tweets)} tweets in the database.")
            # Proceed with sentiment analysis on the existing tweets
            sentiments = get_sentiment_from_db(keyword, start_date, end_date)
            positive_percentage = get_percentage(sentiments)[0]
            negative_percentage = get_percentage(sentiments)[1]
            neutral_percentage = get_percentage(sentiments)[2]
            print(len(sentiments))

                        # Calculate positive and negative summaries  
            # pprint(sentiments)
            positive_tweets = [x for x in sentiments if x['sentiment'] == 'positive']  
            negative_tweets = [x for x in sentiments if x['sentiment']== 'negative']

            print(positive_tweets)
            # negative_tweets = [tweet for tweet in existing_tweets if tweet.sentiment == 'negative']  

            # Get the top 10 positive tweets sorted by likes and retweets  
            top_positive = sorted(positive_tweets, key=lambda x: (x['likes'], x['retweets']), reverse=True)[:10]  
            positive_summary = [{  
                'sentiment': tweet['sentiment'],
                'score':tweet['confidence score'],
                'text': tweet['text'],  
                'likes': tweet['likes'],  
                'retweets': tweet['retweets'] 
            } for tweet in top_positive]  

            # Get the top 10 negative tweets sorted by likes and retweets  
            top_negative = sorted(negative_tweets, key=lambda x: (x['likes'], x['retweets']), reverse=True)[:10]  
            negative_summary = [{  
                'sentiment': tweet['sentiment'],
                'score':tweet['confidence score'],
                'text': tweet['text'],  
                'likes': tweet['likes'],  
                'retweets': tweet['retweets'] 
            } for tweet in top_negative] 
            
            return jsonify({
                'status': 'success',
                'data': sentiments,
                'summary': positive_summary + negative_summary,
                'percentage': f'{positive_percentage:.2f}% Positive, {negative_percentage:.2f}% Negative, {neutral_percentage:.2f}% Neutral',
                'positive summary': positive_summary,
                'negative summary': negative_summary,
                'start date': start_date,
                'end date': end_date
            }), 200
        
        print("test")
        tweet_response = requests.get(FETCH_TWEETS_API_URL, params={
            'min_tweets': min_tweets,  # Minimum number of tweets to fetch (can be adjusted)
            'keyword': keyword,
            'start_date': start_date,
            'end_date': end_date
        })

        # If tweet fetching failed
        if tweet_response.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch tweets from the /fetch_tweets endpoint.'
            }), 500
        
        sentiments = get_sentiment_from_db(keyword, start_date, end_date)
        positive_percentage = get_percentage(sentiments)[0]
        negative_percentage = get_percentage(sentiments)[1]
        neutral_percentage = get_percentage(sentiments)[2]
        positive_tweets = [x for x in sentiments if x['sentiment'] == 'positive']  
        negative_tweets = [x for x in sentiments if x['sentiment']== 'negative']

        print(positive_tweets)
        # negative_tweets = [tweet for tweet in existing_tweets if tweet.sentiment == 'negative']  

        # Get the top 10 positive tweets sorted by likes and retweets  
        top_positive = sorted(positive_tweets, key=lambda x: (x['likes'], x['retweets']), reverse=True)[:10]  
        positive_summary = [{  
            'sentiment': tweet['sentiment'],
            'score':tweet['confidence score'],
            'text': tweet['text'],  
            'likes': tweet['likes'],  
            'retweets': tweet['retweets'] 
        } for tweet in top_positive]  

        # Get the top 10 negative tweets sorted by likes and retweets  
        top_negative = sorted(negative_tweets, key=lambda x: (x['likes'], x['retweets']), reverse=True)[:10]  
        negative_summary = [{  
            'sentiment': tweet['sentiment'],
            'score':tweet['confidence score'],
            'text': tweet['text'],  
            'likes': tweet['likes'],  
            'retweets': tweet['retweets'] 
        } for tweet in top_negative] 
        print('test')

        return jsonify({
                'status': 'success',
                'data': sentiments,
                'summary': positive_summary + negative_summary,
                'percentage': f'{positive_percentage:.2f}% Positive, {negative_percentage:.2f}% Negative, {neutral_percentage:.2f}% Neutral',
                'positive summary': positive_summary,
                'negative summary': negative_summary,
                'start date': start_date,
                'end date': end_date
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def get_percentage(sentiments):
    if isinstance(sentiments, list) and all(isinstance(s, dict) for s in sentiments):  
        sentiments = [s['sentiment'] for s in sentiments]
    sentiment_counts = Counter(sentiments)  # Count each sentiment category
    print(sentiment_counts)
    positive_count = sentiment_counts.get('positive', 0)
    negative_count = sentiment_counts.get('negative', 0)
    neutral_count = sentiment_counts.get('neutral', 0)
    total_sentiments = positive_count + negative_count + neutral_count

    positive_percentage = (positive_count / total_sentiments) * 100 if total_sentiments else 0
    negative_percentage = (negative_count / total_sentiments) * 100 if total_sentiments else 0
    neutral_percentage = (neutral_count / total_sentiments) * 100 if total_sentiments else 0

    return positive_percentage, negative_percentage, neutral_percentage