#!/bin/bash
# Continuous DUSK monitor - keeps bot running 24/7

cd /home/user/DUSKLENDING/dusk-monitor-bot

while true; do
    echo "========================================" >> bot.log
    echo "Starting DUSK monitor at $(date)" >> bot.log
    echo "========================================" >> bot.log

    python3 dusk_monitor.py >> bot.log 2>&1

    echo "Monitor stopped at $(date), restarting in 10 seconds..." >> bot.log
    sleep 10
done
