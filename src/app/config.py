import os

DB_PATH = os.environ.get("NAVIDROME_DB", "../data/navidrome.db")
USE_SAMPLE_DATA = not os.path.exists(DB_PATH)
