from dotenv import load_dotenv
import os

load_dotenv()

def check_api_key(key):
    realkey = os.getenv("FAST_API_KEY")
    return key == realkey