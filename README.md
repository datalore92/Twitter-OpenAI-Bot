# Twitter ChatGPT Bot

A Python bot that automatically interacts with Twitter using ChatGPT.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TwitterChatGPTProject.git
cd TwitterChatGPTProject
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

5. Run the bot:
```bash
python src/main.py
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:
- Twitter API credentials from developer.twitter.com
- OpenAI API key from platform.openai.com

## Features

- Automatically searches for tweets about programming
- Uses ChatGPT to generate responses
- Likes, retweets, and replies to tweets
- Rate limit handling for both Twitter and OpenAI APIs

## Development

- Always activate the virtual environment before running the bot:
```bash
source venv/bin/activate
```

- To deactivate the virtual environment:
```bash
deactivate
```
