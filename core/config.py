import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://hacker-news.firebaseio.com/v0")
HEADERS = {"Content-Type": "application/json"}