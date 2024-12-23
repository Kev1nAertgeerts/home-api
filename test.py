import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("FAST_URL")

r = requests.get(url=f"{BASE_URL}/get-oneday/", json={"date": "2024-12-10"}).json()
print(r["summed_consumptions"])