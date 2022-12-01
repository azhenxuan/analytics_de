#!/bin/bash

python app.py
python repopulate_cache.py

crontab -l | { cat; echo "5 0 1,20 * * ./automate_script.sh"; } | crontab -