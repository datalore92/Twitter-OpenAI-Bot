import time
import asyncio
from services.twitter_service import TwitterService
from services.openai_service import OpenAIService

SEARCH_INTERVAL = 5 * 60  # 5 minutes
SEARCH_QUERY = "your search query here"

twitter_service = TwitterService()
openai_service = OpenAIService()

async def process_new_tweets():
    try:
        tweets = twitter_service.search_tweets(SEARCH_QUERY)
        
        for tweet in tweets.data:
            # Generate response using ChatGPT
            response = await openai_service.generate_response(tweet.text)
            
            # Interact with the tweet
            twitter_service.reply_to_tweet(tweet.id, response)
            twitter_service.like(tweet.id)
            twitter_service.retweet(tweet.id)
            
            # Add delay to avoid rate limits
            await asyncio.sleep(1)
            
    except Exception as error:
        print(f"Error processing tweets: {error}")

async def main():
    print("Starting Twitter Bot...")
    while True:
        await process_new_tweets()
        await asyncio.sleep(SEARCH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
