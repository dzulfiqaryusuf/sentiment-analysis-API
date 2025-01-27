from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    retweets = Column(Integer, default=0)
    likes = Column(Integer, default=0)

    def __repr__(self):
        return f"<Tweet(username={self.username}, created_at={self.created_at})>"
