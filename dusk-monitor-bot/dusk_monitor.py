#!/usr/bin/env python3
"""
DUSK Token Transfer Monitor Bot
Monitors DUSK transfers > 100k and sends Telegram notifications
"""

import os
import time
import asyncio
import aiohttp
from datetime import datetime
from web3 import Web3
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DUSK_CONTRACT = "0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551"
THRESHOLD = 100_000  # 100k DUSK
DUSK_DECIMALS = 18

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ETH_RPC_URL = os.getenv("ETH_RPC_URL")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")

# ERC-20 Transfer event signature
TRANSFER_EVENT_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# Etherscan links
ETHERSCAN_TX = "https://etherscan.io/tx/"
ETHERSCAN_ADDRESS = "https://etherscan.io/address/"

# Known addresses
KNOWN_ADDRESSES = {
    "0x36B8e0B938c0172c20e14cc32E7f0e51dCf1084F": "Mainnet",
}

class DuskMonitor:
    def __init__(self):
        """Initialize the monitor with Web3 and Telegram bot"""
        if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ETH_RPC_URL]):
            raise ValueError("Missing required environment variables. Check .env file.")

        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")

        # Initialize Telegram bot
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

        # Contract setup
        self.contract_address = Web3.to_checksum_address(DUSK_CONTRACT)

        # Minimal ERC-20 ABI for Transfer events
        self.erc20_abi = [
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "from", "type": "address"},
                    {"indexed": True, "name": "to", "type": "address"},
                    {"indexed": False, "name": "value", "type": "uint256"}
                ],
                "name": "Transfer",
                "type": "event"
            }
        ]

        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.erc20_abi
        )

        print("✅ Connected to Ethereum network")
        print(f"✅ Monitoring DUSK contract: {self.contract_address}")
        print(f"✅ Telegram bot ready (Chat ID: {self.chat_id})")
        print(f"🔍 Alert threshold: {THRESHOLD:,} DUSK\n")

    def format_amount(self, value):
        """Convert wei to DUSK tokens"""
        return value / (10 ** DUSK_DECIMALS)

    def format_address(self, address):
        """Format address for display (console only)"""
        return f"{address[:6]}...{address[-4:]}"

    def get_address_label(self, address):
        """Get label for known addresses"""
        # Normalize to checksum address
        try:
            checksum_addr = Web3.to_checksum_address(address)
            return KNOWN_ADDRESSES.get(checksum_addr, None)
        except:
            return None

    async def get_dusk_price(self):
        """Get current DUSK price in USD from CoinGecko"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.coingecko.com/api/v3/simple/price?ids=dusk-network&vs_currencies=usd"
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('dusk-network', {}).get('usd', 0)
        except Exception as e:
            print(f"⚠️  Could not fetch DUSK price: {e}")
        return 0

    async def send_alert(self, tx_hash, from_addr, to_addr, amount):
        """Send Telegram alert for large transfer"""
        amount_formatted = f"{amount:,.2f}"

        # Get current DUSK price in USD
        dusk_price = await self.get_dusk_price()
        usd_value = amount * dusk_price

        # Get address labels
        from_label = self.get_address_label(from_addr)
        to_label = self.get_address_label(to_addr)

        # Format addresses with labels
        from_display = f"<b>{from_label}</b>\n<code>{from_addr}</code>" if from_label else f"<code>{from_addr}</code>"
        to_display = f"<b>{to_label}</b>\n<code>{to_addr}</code>" if to_label else f"<code>{to_addr}</code>"

        # Build message with full addresses and USD value
        message = (
            "🚨 <b>Large DUSK Transfer Detected!</b>\n\n"
            f"💰 <b>Amount:</b> {amount_formatted} DUSK\n"
            f"💵 <b>Value:</b> ${usd_value:,.2f} USD\n\n"
            f"📤 <b>From:</b>\n{from_display}\n\n"
            f"📥 <b>To:</b>\n{to_display}\n\n"
            f"🔗 <b>TX:</b> <a href='{ETHERSCAN_TX}{tx_hash}'>View on Etherscan</a>\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            print(f"✅ Alert sent: {amount_formatted} DUSK (${usd_value:,.2f} USD)")
        except TelegramError as e:
            print(f"❌ Failed to send Telegram message: {e}")

    async def process_transfer(self, event):
        """Process a transfer event"""
        tx_hash = event['transactionHash'].hex()
        from_addr = event['args']['from']
        to_addr = event['args']['to']
        value = event['args']['value']

        amount = self.format_amount(value)

        if amount >= THRESHOLD:
            print(f"\n🔔 LARGE TRANSFER DETECTED!")
            print(f"   Amount: {amount:,.2f} DUSK")
            print(f"   From: {self.format_address(from_addr)}")
            print(f"   To: {self.format_address(to_addr)}")
            print(f"   TX: {tx_hash}")

            await self.send_alert(tx_hash, from_addr, to_addr, amount)

    async def monitor_loop(self):
        """Main monitoring loop"""
        print("🔍 Starting monitor loop...\n")

        # Get the latest block
        latest_block = self.w3.eth.block_number
        last_processed_block = latest_block

        # Send startup message
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"✅ DUSK Monitor Started!\n\nMonitoring transfers > {THRESHOLD:,} DUSK\n"
                     f"Starting from block: {latest_block}",
                parse_mode='HTML'
            )
        except TelegramError as e:
            print(f"⚠️  Could not send startup message: {e}")

        while True:
            try:
                current_block = self.w3.eth.block_number

                # Process new blocks
                if current_block > last_processed_block:
                    # Query transfer events
                    from_block = last_processed_block + 1
                    to_block = current_block

                    print(f"📦 Checking blocks {from_block} to {to_block}...")

                    # Get Transfer events
                    events = self.contract.events.Transfer.get_logs(
                        fromBlock=from_block,
                        toBlock=to_block
                    )

                    if events:
                        print(f"   Found {len(events)} transfer(s)")
                        for event in events:
                            await self.process_transfer(event)

                    last_processed_block = current_block

                # Wait before next check (15 seconds = average block time)
                await asyncio.sleep(15)

            except Exception as e:
                print(f"❌ Error in monitor loop: {e}")
                print("   Retrying in 30 seconds...")
                await asyncio.sleep(30)

    async def run(self):
        """Start the monitor"""
        try:
            await self.monitor_loop()
        except KeyboardInterrupt:
            print("\n\n⚠️  Monitor stopped by user")
            try:
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text="⚠️ DUSK Monitor Stopped",
                    parse_mode='HTML'
                )
            except:
                pass

async def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  DUSK TOKEN TRANSFER MONITOR")
    print("  Real-time alerts for transfers > 100k DUSK")
    print("="*60 + "\n")

    try:
        monitor = DuskMonitor()
        await monitor.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
