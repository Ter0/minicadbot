#!/usr/bin/env bash
# Activate the virtual python environment
source /home/chris/sopel/venv/bin/activate
# Run the bot
sopel -c /home/chris/sopel/minicadbot.cfg
# Deactivate the virtual environment
deactivate

