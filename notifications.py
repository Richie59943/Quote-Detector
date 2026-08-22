import os 
import requests #imports the request library allows us to communicate with api/websites over HTTP 


from dotenv import load_dotenv

load_dotenv()

#this is the end point we are using or trying to reach this is where we send our request to 
PUSHOVER_URL="https://api.pushover.net/1/messages.json"

def send_notification(title,message):
    user_key= os.getenv("PUSHOVER_USER_KEY") #how we enter our .env file and call our api key 
    api_token = os.getenv("PUSHOVER_API_TOKEN")

    if not user_key:
        raise ValueError("PUSHOVER_USER_KEY is missing.")

    if not api_token:
        raise ValueError("PUSHOVER_API_TOKEN is missing.")

        #this is where we create a dictionary that holds data how pushover needs it 
    data = {
        "token": api_token,
        "user": user_key,
        "title":title,
        "message":message,
        "priority": 1,
    }

    #this is when we make a http post rewuest and send data 
    responce = requests.post(
        PUSHOVER_URL,
        data=data,
        timeout=10,
    )

    responce.raise_for_status()

    result = responce.json()

    if result.get("status") != 1:
        raise RuntimeError(
            f"Pushover notification failed: {result}"
        )


    print("Notification sent successfully")

    return True 

if __name__ == "__main__":
    send_notification(
        "Quote Email Monitor",
        "This is a test notification!",
    )
