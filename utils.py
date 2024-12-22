from dotenv import load_dotenv
import os

load_dotenv()

def check_api_key(key):
    realkey = os.getenv("FAST_API_KEY")
    return key == realkey

def create_nested_dict(data):
    result = {}

    for item in data:
        # Extract relevant information
        consumption = item.get("Consumption", {})
        member = consumption.member
        drink = consumption.drink
        
        if member is not None and drink is not None:
            # Initialize the member entry if not present
            if member not in result:   
                result[member] = {}
            
            # Increment the count for the drink
            if drink not in result[member]:
                result[member][drink] = 0
            result[member][drink] += 1

    return result