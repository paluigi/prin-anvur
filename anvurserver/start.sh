#!/bin/sh
cd /app
fastapi run api.py &
supercronic crontab