#!/usr/bin/env python3
"""Test Twitter API authentication"""
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

print("Testing Twitter API connection...")
print(f"API_KEY: {'SET' if API_KEY else 'MISSING'}")
print(f"API_SECRET: {'SET' if API_SECRET else 'MISSING'}")
print(f"ACCESS_TOKEN: {'SET' if ACCESS_TOKEN else 'MISSING'}")
print(f"ACCESS_SECRET: {'SET' if ACCESS_SECRET else 'MISSING'}")
print(f"BEARER_TOKEN: {'SET' if BEARER_TOKEN else 'MISSING'}")
print()

try:
    # Initialize client
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    print("✅ Client initialized")

    # Try to get authenticated user info
    me = client.get_me()
    if me.data:
        print(f"✅ Authenticated as: @{me.data.username}")
        print(f"   Account ID: {me.data.id}")
    else:
        print("❌ Could not get user info")

except Exception as e:
    print(f"❌ Authentication failed: {e}")
    print(f"   Error type: {type(e).__name__}")
