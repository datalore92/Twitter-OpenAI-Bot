import time
import asyncio
from services.twitter_service import TwitterService
from services.openai_service import OpenAIService

SEARCH_INTERVAL = 5 * 60  # 5 minutes
SEARCH_QUERY = "python programming"  # Change this to your desired search term

twitter_service = TwitterService()
openai_service = OpenAIService()

async def process_new_tweets():
    try:
        tweets = twitter_service.search_tweets(SEARCH_QUERY)
        
        if not tweets:
            print("No tweets to process")
            return
            
        for tweet in tweets:
            try:
                print(f"\nProcessing tweet: {tweet.text[:50]}...")
                
                # Add longer delay between tweets
                await asyncio.sleep(5)  
                
                response = await openai_service.generate_response(tweet.text)
                if response:
                    print(f"Generated response: {response}")
                    
                    twitter_service.reply_to_tweet(tweet.id, response)
                    print(f"Reply posted to tweet {tweet.id}")
                    
                    # Add delay between actions
                    await asyncio.sleep(2)
                    
                    twitter_service.like(tweet.id)
                    print(f"Liked tweet {tweet.id}")
                    
                    await asyncio.sleep(2)
                    
                    twitter_service.retweet(tweet.id)
                    print(f"Retweeted tweet {tweet.id}")
                    
                    # Longer delay after full interaction
                    await asyncio.sleep(10)
                
            except Exception as e:
                print(f"Error processing individual tweet: {e}")
                await asyncio.sleep(5)  # Wait before next tweet on error
                continue

    except Exception as error:
        print(f"Error in process_new_tweets: {error}")
        await asyncio.sleep(30)  # Longer wait on major error

async def main():
    print("Starting Twitter Bot...")
    while True:
        await process_new_tweets()
        await asyncio.sleep(SEARCH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
