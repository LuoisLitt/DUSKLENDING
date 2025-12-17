#!/usr/bin/env python3
"""Send a test alert to Telegram"""

import os
import asyncio
import aiohttp
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Known addresses
KNOWN_ADDRESSES = {
    "0x36B8e0B938c0172c20e14cc32E7f0e51dCf1084F": "Mainnet",
}

def get_address_label(address):
    """Get label for known addresses"""
    try:
        checksum_addr = Web3.to_checksum_address(address)
        return KNOWN_ADDRESSES.get(checksum_addr, None)
    except:
        return None

async def send_test_alert():
    """Send a test DUSK transfer alert"""

    # Get configuration
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Example data - using Mainnet address
    amount = 150_000.00
    tx_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    from_addr = "0x36B8e0B938c0172c20e14cc32E7f0e51dCf1084F"  # Mainnet
    to_addr = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"

    # Get DUSK price
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=dusk-network&vs_currencies=usd"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    dusk_price = data.get('dusk-network', {}).get('usd', 0.165)
                else:
                    dusk_price = 0.165  # Fallback price
    except:
        dusk_price = 0.165  # Fallback price

    usd_value = amount * dusk_price

    # Get address labels
    from_label = get_address_label(from_addr)
    to_label = get_address_label(to_addr)

    # Format addresses with labels
    from_display = f"<b>{from_label}</b>\n<code>{from_addr}</code>" if from_label else f"<code>{from_addr}</code>"
    to_display = f"<b>{to_label}</b>\n<code>{to_addr}</code>" if to_label else f"<code>{to_addr}</code>"

    # Build message
    message = (
        "🚨 <b>Large DUSK Transfer Detected!</b>\n"
        "<i>(This is a TEST alert)</i>\n\n"
        f"💰 <b>Amount:</b> {amount:,.2f} DUSK\n"
        f"💵 <b>Value:</b> ${usd_value:,.2f} USD\n\n"
        f"📤 <b>From:</b>\n{from_display}\n\n"
        f"📥 <b>To:</b>\n{to_display}\n\n"
        f"🔗 <b>TX:</b> <a href='https://etherscan.io/tx/{tx_hash}'>View on Etherscan</a>\n"
        f"⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    # Send message
    bot = Bot(token=bot_token)
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

    print("✅ Test alert sent to Telegram!")

if __name__ == "__main__":
    asyncio.run(send_test_alert())
