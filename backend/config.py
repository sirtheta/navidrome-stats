import os

DB_PATH = os.environ.get("NAVIDROME_DB", "/data/navidrome.db")
USE_SAMPLE_DATA = not os.path.exists(DB_PATH)
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
