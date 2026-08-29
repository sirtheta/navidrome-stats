#!/bin/sh
uv run pybabel compile -d translations
uv run fastapi run --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="*"
