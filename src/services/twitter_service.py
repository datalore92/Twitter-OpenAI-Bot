import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime

class TwitterService:
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret, self.bearer_token]):
            raise ValueError("Missing Twitter credentials")

        try:
            # V2 Client with both OAuth 1.0a and Bearer Token
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret,
                wait_on_rate_limit=True
            )
            
            # Test the authentication
            me = self.client.get_me()
            print(f"Twitter authentication successful! Logged in as: {me.data.username}")
            
        except Exception as e:
            print(f"Twitter authentication failed: {str(e)}")
            raise

    def get_rate_limit_status(self):
        """Get detailed rate limit information from response headers"""
        try:
            # Make a test request to get rate limit headers
            response = self.client.search_recent_tweets(
                query="test",
                max_results=1
            )
            
            # Get rate limit info from headers
            headers = response.includes
            
            print("\n=== Twitter Rate Limits ===")
            print(f"Remaining requests: {response.meta.get('remaining', 'N/A')}")
            print(f"Rate limit: {response.meta.get('limit', 'N/A')}")
            print(f"Reset time: {response.meta.get('reset', 'N/A')}")
            print("========================\n")
            
        except tweepy.TooManyRequests as e:
            reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
            wait_time = reset_time - int(datetime.now().timestamp())
            print(f"\n!!! Twitter Rate Limit Exceeded !!!")
            print(f"Reset Time: {datetime.fromtimestamp(reset_time)}")
            print(f"Wait Time: {wait_time} seconds")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        except Exception as e:
            print(f"Could not fetch rate limits: {str(e)}")

    def format_reset_time(self, reset_time):
        if reset_time:
            now = datetime.now().timestamp()
            return max(0, int(reset_time - now))
        return 'unknown'

    def search_tweets(self, query):
        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['author_id', 'created_at', 'text'],
                expansions=['author_id']
            )
            
            # Print rate limit info from response
            if hasattr(response, 'meta'):
                print("\n=== Search Request Rate Limits ===")
                print(f"Remaining: {response.meta.get('remaining', 'N/A')}")
                print(f"Limit: {response.meta.get('limit', 'N/A')}")
                print(f"Reset: {response.meta.get('reset', 'N/A')}")
                print("==============================\n")
            
            if not response.data:
                print(f"No tweets found for query: {query}")
                return []
            
            print(f"Found {len(response.data)} tweets")
            return response.data
            
        except tweepy.TooManyRequests as e:
            reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
            wait_time = reset_time - int(datetime.now().timestamp())
            print(f"\n!!! Twitter Rate Limit Exceeded !!!")
            print(f"Endpoint: Search Tweets")
            print(f"Reset Time: {datetime.fromtimestamp(reset_time)}")
            print(f"Wait Time: {wait_time} seconds")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            return []
        except Exception as e:
            print(f"Twitter API error: {str(e)}")
            return []

    def reply_to_tweet(self, tweet_id, content):
        return self.client.create_tweet(text=content, in_reply_to_tweet_id=tweet_id)

    def retweet(self, tweet_id):
        return self.client.retweet(tweet_id)

    def like(self, tweet_id):
        return self.client.like(tweet_id)
