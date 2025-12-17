#!/bin/bash
# Continuous bot runner - keeps restarting the bot

cd /home/user/DUSKLENDING/dusk-twitter-bot

while true; do
    echo "========================================" >> bot.log
    echo "Starting bot at $(date)" >> bot.log
    echo "========================================" >> bot.log

    python3 dusk_bot.py >> bot.log 2>&1

    echo "Bot stopped at $(date), restarting in 60 seconds..." >> bot.log
    sleep 60
done
