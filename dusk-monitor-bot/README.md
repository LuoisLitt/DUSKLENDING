# DUSK Token Transfer Monitor Bot

Real-time Telegram notifications for large DUSK token transfers (>100k DUSK).

## Features

- 🔍 **Real-time monitoring** of DUSK token transfers on Ethereum mainnet
- 📱 **Telegram alerts** for transfers exceeding 100,000 DUSK
- 🔄 **Continuous operation** - runs 24/7 with auto-restart
- 💰 **Detailed transaction info** - full addresses, DUSK amount, USD value, Etherscan links
- 💵 **Live USD pricing** - fetches current DUSK price from CoinGecko
- ⚡ **Fast detection** - checks new blocks every 15 seconds

## Prerequisites

1. **Telegram Bot Token**
   - Talk to [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Save your bot token

2. **Telegram Chat ID**
   - Start a chat with your bot
   - Send any message to it
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id":123456789}` - that's your chat ID

3. **Ethereum RPC Endpoint**
   - Get free API key from [Alchemy](https://www.alchemy.com/) or [Infura](https://www.infura.io/)
   - Create an Ethereum Mainnet app
   - Copy the HTTPS endpoint URL

## Setup

### 1. Install Dependencies

```bash
cd /home/user/DUSKLENDING/dusk-monitor-bot
pip3 install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Ethereum RPC Configuration
ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
```

### 3. Test the Bot

```bash
# Test run (will stop with Ctrl+C)
python3 dusk_monitor.py
```

You should see:
- ✅ Connected to Ethereum network
- ✅ Monitoring DUSK contract
- ✅ Telegram bot ready
- Telegram message: "DUSK Monitor Started!"

### 4. Run Continuously (24/7)

```bash
nohup ./run_continuous.sh > /dev/null 2>&1 &
```

The bot will now run in the background and automatically restart if it stops.

## Usage

### Monitor the Bot

```bash
# View live activity
tail -f bot.log

# Check if bot is running
ps aux | grep dusk_monitor.py

# View recent logs
tail -50 bot.log
```

### Stop the Bot

```bash
pkill -f dusk_monitor.py
pkill -f run_continuous.sh
```

### Restart the Bot

```bash
# Stop first
pkill -f dusk_monitor.py && pkill -f run_continuous.sh

# Start again
nohup ./run_continuous.sh > /dev/null 2>&1 &
```

## Alert Format

When a large transfer is detected, you'll receive a Telegram message like:

```
🚨 Large DUSK Transfer Detected!

💰 Amount: 150,000.00 DUSK
💵 Value: $24,750.00 USD

📤 From:
0x1234567890123456789012345678901234567890

📥 To:
0xabcdefabcdefabcdefabcdefabcdefabcdefabcd

🔗 TX: View on Etherscan
⏰ Time: 2025-12-17 14:30:45 UTC
```

## Configuration

### Change Alert Threshold

Edit `dusk_monitor.py` line 20:

```python
THRESHOLD = 100_000  # Change to your preferred amount
```

### Change Monitoring Interval

Edit `dusk_monitor.py` line 169:

```python
await asyncio.sleep(15)  # Change from 15 seconds
```

## Monitored Contract

- **Token:** DUSK Network Token
- **Contract:** `0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551`
- **Network:** Ethereum Mainnet
- **Decimals:** 18

## Troubleshooting

### "Failed to connect to Ethereum node"
- Check your `ETH_RPC_URL` is correct
- Verify your Alchemy/Infura API key is valid
- Test the URL in a browser

### "Failed to send Telegram message"
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check `TELEGRAM_CHAT_ID` is your actual chat ID
- Make sure you've started a chat with the bot

### Bot not detecting transfers
- Check the bot is running: `ps aux | grep dusk_monitor.py`
- View logs: `tail -f bot.log`
- Verify RPC connection is working
- Check Ethereum network isn't experiencing issues

### Bot keeps stopping
- Check logs for errors: `tail -100 bot.log`
- Ensure `run_continuous.sh` is running: `ps aux | grep run_continuous`
- Verify RPC endpoint has enough credits/requests

## Files

- `dusk_monitor.py` - Main bot script
- `run_continuous.sh` - Keeps bot running 24/7
- `.env` - Your private configuration (not committed to git)
- `.env.example` - Template for environment variables
- `requirements.txt` - Python dependencies
- `bot.log` - Activity logs

## Security

- ⚠️ Never commit `.env` file to git (it contains your private keys)
- ⚠️ Keep your Telegram bot token secret
- ⚠️ Don't share your chat ID publicly

## License

MIT License - Free to use and modify.
