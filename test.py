import requests
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

BASE_URL = os.getenv("FAST_URL")

r = requests.post(url=f"{BASE_URL}/delete-consumption/", json={"member":"Jef", "drink":"Cola"}).json()
#print(date.today())