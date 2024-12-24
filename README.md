# Twitter ChatGPT Bot

A Python bot that automatically interacts with Twitter using ChatGPT.

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
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

4. Configure environment variables in `.env` file:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
OPENAI_API_KEY=your_openai_api_key
```

5. Run the bot:
```bash
python src/main.py
```

## Development

- Always activate the virtual environment before running the bot:
```bash
source venv/bin/activate
```

- To deactivate the virtual environment:
```bash
deactivate
```
