# Dusk Network Twitter Growth Bot

Automated Twitter bot for promoting Dusk Network with authentic content about privacy-preserving blockchain technology, institutional DeFi, and real-world asset tokenization.

## Features

- **Automated Posting**: Schedules 30+ tweets per day at optimal times
- **Thread Support**: Posts educational thread series about Dusk technology
- **Smart Engagement**: Likes and retweets content from relevant accounts
- **Analytics Tracking**: Monitors posting statistics over time
- **Content Variety**: Multiple tweet templates covering:
  - Hot takes on RWA and privacy
  - Educational content about ZK technology
  - Dusk milestones and achievements
  - Engagement-driving questions
  - Problem/solution frameworks

## Prerequisites

- Python 3.7+
- Twitter Developer Account with API access
- Twitter API v2 credentials (API Key, Secret, Access Tokens, Bearer Token)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd dusk-twitter-bot
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` and add your Twitter API credentials:**
   ```
   TWITTER_API_KEY=your_actual_api_key
   TWITTER_API_SECRET=your_actual_api_secret
   TWITTER_ACCESS_TOKEN=your_actual_access_token
   TWITTER_ACCESS_SECRET=your_actual_access_secret
   TWITTER_BEARER_TOKEN=your_actual_bearer_token
   ```

## Getting Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. Navigate to "Keys and Tokens"
4. Generate/copy:
   - API Key and Secret
   - Access Token and Secret
   - Bearer Token
5. Ensure your app has **Read and Write** permissions

## Usage

### Preview Mode (Test without posting)

See sample tweets without actually posting to Twitter:

```bash
python dusk_bot.py preview
```

### Live Mode (Real posting)

Run the bot to post tweets throughout the day:

```bash
python dusk_bot.py
```

**Note:** The bot will wait for scheduled times before posting. It's designed to run for a full day cycle.

### Running in Background (Linux/Mac)

Use `nohup` or `screen` to keep it running:

```bash
# Using nohup
nohup python dusk_bot.py > bot.log 2>&1 &

# Using screen
screen -S dusk-bot
python dusk_bot.py
# Press Ctrl+A then D to detach
```

## Configuration

Edit these variables in `dusk_bot.py` or via environment variables:

- `DAILY_FOLLOW_LIMIT`: Maximum accounts to engage with per day (default: 50)
- `ANALYTICS_FILE`: File to store posting statistics (default: `dusk_twitter_analytics.json`)

### Scheduling

The bot posts during "prime hours" (8am, 10am, 12pm, 2pm, 4pm, 6pm, 8pm, 10pm) with:
- 30 regular tweets distributed throughout the day
- 2 threads (at 10:00am and 7:30pm)
- Engagement actions every 5 posts

## Content Management

### Adding New Content

Edit these lists in `dusk_bot.py`:

- `DUSK_FACTS`: Key facts about Dusk Network
- `DUSK_TECH_DETAILS`: Technical details and features
- `INSTITUTIONAL_PROBLEMS`: Problems institutions face
- `DUSK_ADVANTAGES`: How Dusk solves these problems
- `TWEET_TEMPLATES`: Tweet format templates
- `THREAD_STARTERS`: Pre-written thread series

### Customizing Tweet Mix

Adjust weights in `generate_tweet()` function:

```python
weights = {
    "hot_takes": 0.20,        # 20% hot takes
    "engagement_bait": 0.20,  # 20% engagement
    "dusk_milestones": 0.20,  # 20% milestones
    # ... etc
}
```

## Safety & Best Practices

⚠️ **Important:**

- Never commit your `.env` file with real credentials
- Start with preview mode to test content
- Monitor your Twitter account for the first few hours
- Be aware of Twitter's rate limits and automation rules
- Keep `DAILY_FOLLOW_LIMIT` conservative to avoid restrictions
- Review Twitter's [Automation Rules](https://help.twitter.com/en/rules-and-policies/twitter-automation)

## Analytics

The bot tracks:
- Total tweets posted
- Last run timestamp
- Daily posting count

View analytics in `dusk_twitter_analytics.json`

## Troubleshooting

### "Missing required Twitter API credentials"
- Check that your `.env` file exists and has all 5 credentials
- Ensure `.env` is in the same directory as `dusk_bot.py`

### API Rate Limit Errors
- The bot uses `wait_on_rate_limit=True` to handle this automatically
- If persistent, reduce posting frequency

### Connection Errors
- Check your internet connection
- Verify Twitter API status at [Twitter API Status](https://api.twitterstat.us/)

## License

MIT License - feel free to modify and use for your own projects.

## Disclaimer

This bot is for educational and promotional purposes. Use responsibly and in compliance with Twitter's Terms of Service and Automation Rules. The creators are not responsible for any account restrictions resulting from misuse.

## Support

For issues or questions about Dusk Network, visit:
- [Dusk Foundation](https://dusk.network/)
- [Dusk Twitter](https://twitter.com/DuskFoundation)
- [Dusk Documentation](https://docs.dusk.network/)
