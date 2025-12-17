#!/usr/bin/env python3
"""
Helper script to get your Telegram Chat ID
Run this after you've sent a message to your bot
"""

import os
import sys
from dotenv import load_dotenv

try:
    from telegram import Bot
    import asyncio
except ImportError:
    print("❌ Please install requirements first:")
    print("   pip3 install -r requirements.txt")
    sys.exit(1)

load_dotenv()

async def get_chat_id():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set TELEGRAM_BOT_TOKEN in .env file first")
        print("\n1. Talk to @BotFather on Telegram")
        print("2. Send /newbot and follow instructions")
        print("3. Copy the token to .env file")
        return

    try:
        bot = Bot(token=token)
        updates = await bot.get_updates()

        if not updates:
            print("❌ No messages found!")
            print("\nPlease:")
            print("1. Open Telegram and search for your bot")
            print("2. Send any message to your bot")
            print("3. Run this script again")
            return

        print("\n✅ Found your chats:\n")
        for update in updates:
            if update.message:
                chat = update.message.chat
                print(f"Chat ID: {chat.id}")
                print(f"Type: {chat.type}")
                if chat.username:
                    print(f"Username: @{chat.username}")
                if chat.first_name:
                    print(f"Name: {chat.first_name}")
                print("-" * 40)

        print("\n✅ Copy the Chat ID above to your .env file:")
        print(f"   TELEGRAM_CHAT_ID={updates[0].message.chat.id}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure your bot token is correct!")

if __name__ == "__main__":
    print("=" * 50)
    print("  TELEGRAM CHAT ID FINDER")
    print("=" * 50 + "\n")
    asyncio.run(get_chat_id())
