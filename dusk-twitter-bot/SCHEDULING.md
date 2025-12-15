# Scheduling the Dusk Twitter Bot to Run Daily at 7 AM

This guide provides multiple methods to automatically run the bot every day at 7:00 AM.

## Option 1: Using Cron (Recommended for Most Users)

### Setup Cron Job

1. **Make the run script executable:**
   ```bash
   chmod +x run_bot.sh
   ```

2. **Open your crontab editor:**
   ```bash
   crontab -e
   ```

3. **Add this line to run the bot daily at 7 AM:**
   ```
   0 7 * * * /home/user/DUSKLENDING/dusk-twitter-bot/run_bot.sh
   ```

4. **Save and exit** (Ctrl+O, Enter, Ctrl+X for nano)

### Verify Cron Job

Check that your cron job is installed:
```bash
crontab -l
```

### View Logs

Logs are stored in `bot_logs/` directory with timestamps:
```bash
tail -f bot_logs/run_*.log
```

## Option 2: Using Systemd Timer (For Linux Systems)

### Setup Systemd Timer

1. **Make the run script executable:**
   ```bash
   chmod +x run_bot.sh
   ```

2. **Update paths in service files** (if your path differs):
   - Edit `dusk-twitter-bot.service`
   - Edit `dusk-twitter-bot.timer`
   - Replace `/home/user/` with your actual home directory

3. **Copy service files to systemd:**
   ```bash
   sudo cp dusk-twitter-bot.service /etc/systemd/system/
   sudo cp dusk-twitter-bot.timer /etc/systemd/system/
   ```

4. **Reload systemd and enable the timer:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable dusk-twitter-bot.timer
   sudo systemctl start dusk-twitter-bot.timer
   ```

### Manage Systemd Timer

**Check timer status:**
```bash
sudo systemctl status dusk-twitter-bot.timer
```

**See when the timer will run next:**
```bash
sudo systemctl list-timers dusk-twitter-bot.timer
```

**View bot logs:**
```bash
sudo journalctl -u dusk-twitter-bot.service -f
```

**Manually trigger the bot (for testing):**
```bash
sudo systemctl start dusk-twitter-bot.service
```

**Stop the timer:**
```bash
sudo systemctl stop dusk-twitter-bot.timer
sudo systemctl disable dusk-twitter-bot.timer
```

## Option 3: Manual Run with Screen (For Testing)

Run the bot in a screen session that persists after logout:

```bash
# Create a new screen session
screen -S dusk-bot

# Navigate to bot directory
cd /home/user/DUSKLENDING/dusk-twitter-bot

# Run the bot
python3 dusk_bot.py

# Detach from screen: Press Ctrl+A, then D
```

**Reattach to the session later:**
```bash
screen -r dusk-bot
```

## Timezone Considerations

All scheduling methods use your system's local timezone. To check your timezone:

```bash
timedatectl
```

To change timezone (if needed):
```bash
sudo timedatectl set-timezone America/New_York
# Or: Europe/London, Asia/Tokyo, etc.
```

**For UTC scheduling** (recommended for global reach):
```bash
sudo timedatectl set-timezone UTC
```

## Log Management

The `run_bot.sh` script automatically:
- Creates logs in `bot_logs/` directory
- Names logs with timestamps: `run_YYYYMMDD_HHMMSS.log`
- Keeps logs for 30 days (older logs are auto-deleted)

### View Recent Logs

```bash
# View latest log
cat bot_logs/run_*.log | tail -n 50

# View all logs from today
cat bot_logs/run_$(date +%Y%m%d)_*.log

# Monitor live output
tail -f bot_logs/run_*.log
```

## Troubleshooting

### Bot Not Running

1. **Check cron is running:**
   ```bash
   sudo systemctl status cron
   ```

2. **Check cron logs:**
   ```bash
   grep CRON /var/log/syslog | tail
   ```

3. **Test the script manually:**
   ```bash
   cd /home/user/DUSKLENDING/dusk-twitter-bot
   ./run_bot.sh
   ```

### Permission Issues

If you get permission errors:
```bash
chmod +x run_bot.sh
chmod +x dusk_bot.py
```

### Python Module Not Found

If the bot can't find tweepy or other modules:

1. **Install in your user environment:**
   ```bash
   pip3 install --user -r requirements.txt
   ```

2. **Or use a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Then update `run_bot.sh` to activate the venv (it already has this code).

### API Credential Errors

Ensure your `.env` file exists and has valid credentials:
```bash
cat .env
```

Should contain:
```
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## Best Practices

1. **Test first**: Run the bot manually before scheduling
2. **Monitor logs**: Check logs after first few scheduled runs
3. **Set timezone to UTC**: For consistent global timing
4. **Use systemd over cron**: If you need better logging and management
5. **Keep credentials secure**: Never commit `.env` to git

## Changing the Schedule

### Cron Schedule Examples

```bash
# Run at 7 AM daily
0 7 * * *

# Run at 9:30 AM daily
30 9 * * *

# Run at 7 AM on weekdays only
0 7 * * 1-5

# Run twice daily (7 AM and 7 PM)
0 7,19 * * *
```

### Systemd Timer Schedule Examples

Edit `dusk-twitter-bot.timer` and change the `OnCalendar` line:

```ini
# Daily at 7 AM
OnCalendar=*-*-* 07:00:00

# Daily at 9:30 AM
OnCalendar=*-*-* 09:30:00

# Weekdays at 7 AM
OnCalendar=Mon-Fri *-*-* 07:00:00

# Twice daily (7 AM and 7 PM)
OnCalendar=*-*-* 07:00:00
OnCalendar=*-*-* 19:00:00
```

After changing the timer, reload systemd:
```bash
sudo systemctl daemon-reload
sudo systemctl restart dusk-twitter-bot.timer
```
