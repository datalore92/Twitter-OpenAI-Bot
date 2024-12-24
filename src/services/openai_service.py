import openai
import os
import random
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv  # Add this import

class OpenAIService:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.last_call_time = 0
        self.min_delay = 3  # Minimum seconds between API calls
        self.fallback_responses = [
            "Thanks for sharing! This is interesting 👍",
            "Great point! Thanks for sharing 🙌",
            "Interesting perspective on this 🤔",
            "Thanks for the info! 💡",
            "Nice share! Keep it up 🚀"
        ]
        self.requests_this_minute = 0
        self.last_request_minute = datetime.now().minute
        self.max_requests_per_minute = 3  # Adjust based on your plan
        self.total_requests = 0
        self.start_time = datetime.now()

    def print_usage_stats(self):
        """Print detailed usage statistics"""
        current_time = datetime.now()
        uptime = (current_time - self.start_time).total_seconds()
        
        print("\n=== OpenAI Usage Stats ===")
        print(f"Total requests: {self.total_requests}")
        print(f"Uptime: {int(uptime)} seconds")
        print(f"Requests this minute: {self.requests_this_minute}/{self.max_requests_per_minute}")
        print(f"Rate: {self.total_requests / (uptime / 3600):.2f} requests/hour")
        print(f"Next minute reset in: {60 - datetime.now().second} seconds")
        print("=======================\n")

    async def generate_response(self, context):
        try:
            self.print_usage_stats()
            
            # Rate limit tracking
            current_minute = datetime.now().minute
            if current_minute != self.last_request_minute:
                print("=== Rate Limit Reset ===")
                print(f"New minute started, resetting counter from {self.requests_this_minute} to 0")
                self.requests_this_minute = 0
                self.last_request_minute = current_minute

            if self.requests_this_minute >= self.max_requests_per_minute:
                print("\n!!! OpenAI Rate Limit Reached !!!")
                print(f"Current minute: {self.requests_this_minute}/{self.max_requests_per_minute} requests")
                print(f"Next reset in: {60 - datetime.now().second} seconds")
                print("Using fallback response")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                return random.choice(self.fallback_responses)

            self.requests_this_minute += 1
            self.total_requests += 1

            print(f"\nOpenAI Rate Limits:")
            print(f"Requests this minute: {self.requests_this_minute}/{self.max_requests_per_minute}")
            print(f"Next reset in: {60 - datetime.now().second} seconds\n")

            # Rate limiting
            current_time = time.time()
            time_since_last_call = current_time - self.last_call_time
            if time_since_last_call < self.min_delay:
                await asyncio.sleep(self.min_delay - time_since_last_call)
            
            self.last_call_time = time.time()

            # More efficient prompt with fewer tokens
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a friendly Twitter user. Keep responses short and engaging."
                }, {
                    "role": "user",
                    "content": f"Reply to: {context[:100]}"  # Limit context length
                }],
                max_tokens=30,  # Reduced from 60
                temperature=0.7
            )
            return completion.choices[0].message.content

        except openai.error.RateLimitError as e:
            print("\n!!! OpenAI Quota Exceeded !!!")
            print(f"Error: {str(e)}")
            print("Using fallback response")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            return random.choice(self.fallback_responses)
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return random.choice(self.fallback_responses)
