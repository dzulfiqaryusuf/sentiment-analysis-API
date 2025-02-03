from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    scraped_id = Column(String(255),unique=True, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    retweets = Column(Integer, default=0)
    likes = Column(Integer, default=0)

    def __repr__(self):
        return f"<Tweet(id={self.id}, scraped_id={self.scraped_id}, text={self.text}, created_at={self.created_at})>, retweets={self.retweets}, likes={self.likes}"
