#!/bin/bash
# Dusk Twitter Bot - Daily Runner Script
# This script should be scheduled to run daily at 7 AM

# Set the working directory to the bot location
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Log file with timestamp
LOG_FILE="bot_logs/run_$(date +%Y%m%d_%H%M%S).log"
mkdir -p bot_logs

# Run the bot and log output
echo "========================================" | tee -a "$LOG_FILE"
echo "Starting Dusk Twitter Bot" | tee -a "$LOG_FILE"
echo "Time: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

python3 dusk_bot.py 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "Bot session completed at $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Keep only last 30 days of logs
find bot_logs -name "run_*.log" -mtime +30 -delete
