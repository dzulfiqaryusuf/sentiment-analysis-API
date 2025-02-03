from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
from models.tweet_model import Tweet
from models.sentiment_model import Sentiment
from utils.db import SessionLocal
from scipy.special import softmax
import numpy as np


MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

QUERY = 'mytelkomsel'
QUERY2 = 'telkomsel'
#/ save the model locally
# model.save_pretrained("./cardiffnlp/twitter-xlm-roberta-base-sentiment")
# tokenizer.save_pretrained("./cardiffnlp/twitter-xlm-roberta-base-sentiment")

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_sentiment(text: str) -> str:
    processed_text = preprocess(text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    index_of_sentiment = output.logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    scores = output[0][0].detach().numpy()
    sentiment_score = max(softmax(scores))
    return sentiment,sentiment_score


def get_sentiment_from_db(keyword, start_date, end_date):
    session = SessionLocal()
    try:
        # Query the last 100 tweets from the database
        tweets = session.query(Tweet).filter(Tweet.text.ilike(f'%{keyword}%')).filter(Tweet.created_at >= start_date).filter(Tweet.created_at <= end_date).order_by(Tweet.created_at.desc()).limit(200).all()
        sentiments = []

        for tweet in tweets:
            # Check if sentiment already exists in the database for this tweet
            existing_sentiment = session.query(Sentiment).filter(Sentiment.tweet_id == tweet.id).first()
            
            if existing_sentiment:
                # If sentiment exists, use it
                sentiment = existing_sentiment.sentiment_type
                score = existing_sentiment.sentiment_score
            else:
                # If no sentiment data, run sentiment analysis
                sentiment_and_score = predict_sentiment(tweet.text)
                sentiment = sentiment_and_score[0]
                score = sentiment_and_score[1]
                
                # Save the sentiment to the Sentiment table in the database
                new_sentiment = Sentiment(
                    tweet_id=tweet.id,
                    sentiment_type=sentiment,
                    sentiment_score=round(float(score), 2),
                    model_name=MODEL  # You can save the model name too if needed
                )
                session.add(new_sentiment)
                session.commit()
                
            sentiments.append({
                'tweet_id': tweet.id,
                'text': tweet.text,
                'sentiment': sentiment,
                'confidence score': round(float(score), 2),
                'likes': tweet.likes,
                'retweets': tweet.retweets
            })

        return sentiments
    finally:
        session.close()

def update_sentiments_in_db(sentiments):
    session = SessionLocal()
    try:
        for sentiment in sentiments:
            tweet = session.query(Tweet).filter(Tweet.text)
            if tweet:
                tweet.sentiment = sentiment['sentiment']
        session.commit()
    finally:
        session.close()

# Initialize the sentiment analysis pipeline

# def analyze_sentiment():
#     session = SessionLocal()
#     try:
#         tweets = session.query(Tweet).order_by(Tweet.created_at.desc()).limit(100).all()

#         return sentiments
#     finally:
#         session.close()
