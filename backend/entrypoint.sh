#!/bin/sh
uv run gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 4 app:app
