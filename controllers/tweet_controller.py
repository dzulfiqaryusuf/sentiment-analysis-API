from flask import Blueprint, jsonify, request
from services.tweet_service import fetch_and_store_tweets
from datetime import datetime
import pytz
import asyncio

timezone = pytz.timezone('Asia/Jakarta')
now = datetime.now(timezone)
tweet_bp = Blueprint('tweets', __name__)

def get_start_date(end_date: datetime):
    # Set start_date to the 1st day of the same month as the end_date
    return end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

@tweet_bp.route('/fetch_tweets', methods=['GET'])
def fetch_tweets():
    try:
        min_tweets = request.args.get('min_tweets', 200)
        keyword = request.args.get('keyword', '')
        end_date = request.args.get('end_date', datetime.now(timezone))
        start_date = request.args.get('start_date', datetime(now.year, now.month, 1, 0, 0, 0, 0))
        print(f'Start date: {start_date}, End date: {end_date}')
        print(f'Minimum tweets: {min_tweets}, Keyword: {keyword}')

        tweet_count = asyncio.run(fetch_and_store_tweets(min_tweets,keyword, start_date, end_date))
        return jsonify({
            'status': 'success',
            'message': f'Fetched and stored {tweet_count} tweets.'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

