from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models import Base
from models.tweet_model import Tweet
from sqlalchemy.orm import relationship

class Sentiment(Base):
    __tablename__ = 'sentiments'
    sentiment_id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=False)
    sentiment_type = Column(String(50), nullable=False)
    sentiment_score = Column(Float, nullable=False)
    model_name = Column(String(255), nullable=True)
    tweet = relationship('Tweet', backref='sentiments')
    def __repr__(self):
        return f"<Sentiment(tweet_id={self.tweet_id}, sentiment_type={self.sentiment_type}, sentiment_score={self.sentiment_score}, model_name={self.model_name})>"
