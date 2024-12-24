import tweepy
import os
from dotenv import load_dotenv

class TwitterService:
    def __init__(self):
        load_dotenv()
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_SECRET')
        )
        self.api = tweepy.API(auth)
        self.client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
        )

    def search_tweets(self, query):
        return self.client.search_recent_tweets(query=query, max_results=10)

    def reply_to_tweet(self, tweet_id, content):
        return self.client.create_tweet(text=content, in_reply_to_tweet_id=tweet_id)

    def retweet(self, tweet_id):
        return self.client.retweet(tweet_id)

    def like(self, tweet_id):
        return self.client.like(tweet_id)
