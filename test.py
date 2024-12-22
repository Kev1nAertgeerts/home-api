import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("FAST_URL")

print(requests.get(url=f"{BASE_URL}/get-members/").json())