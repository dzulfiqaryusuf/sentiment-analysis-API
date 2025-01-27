from flask import Blueprint, jsonify, request
from services.tweet_service import fetch_and_store_tweets
from services.sentiment_service import analyze_sentiment

tweet_bp = Blueprint('tweets', __name__)

@tweet_bp.route('/fetch_tweets', methods=['POST'])
def fetch_tweets():
    try:
        min_tweets = request.json.get('min_tweets', 20)
        tweet_count = fetch_and_store_tweets(min_tweets)
        return jsonify({
            'status': 'success',
            'message': f'Fetched and stored {tweet_count} tweets.'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@tweet_bp.route('/analyze_sentiment', methods=['GET'])
def sentiment():
    try:
        # Example: Analyze sentiment for the latest tweets
        sentiments = analyze_sentiment()
        return jsonify({
            'status': 'success',
            'data': sentiments
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
