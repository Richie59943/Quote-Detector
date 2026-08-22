import os.path
import json
import base64 #google stores messages of emails in base 64 encoding so we have to decode
from quote_detector import get_quote_score, is_quote_request
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials #this allows us to load saved Google login permissions 
from google_auth_oauthlib.flow import InstalledAppFlow #handles google login window 
from googleapiclient.discovery import build  # this is what allows Gmail API connect to python and GMAIL 
from notifications import send_notification
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"] #we are only allowing our code to read emails (possibly change to send)


def get_gmail_service():
    #assumes our crednetials are 0 right now 
    creds= None 

    if os.path.exists("token.json"): #checks if our file token.json is in our folder 
        creds= Credentials.from_authorized_user_file("token.json", SCOPES) #loads previous auth into python 

        # if we dont have credentials or they expired we prompt log in again 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES 
            )

            #opens our browser 
            creds = flow.run_local_server(port=0)

        #opens our file the token,json and allows us to write in there 
        with open("token.json", "w") as token:
            token.write(creds.to_json()) #write out tokens

    #this is going to act as of remote control for gmail creates the gmail connection 
    service =build("gmail", "v1", credentials=creds)

    return service 

#payload contains headers, body, parts, attachments,mime types 
def get_email_body(payload):
    #sets our body to ""
    body=""

    #checks if email contains extrta parts 
    if "parts" in payload:
        for part in payload["parts"]:
            #mimetpe tells us which kind of data something is either text plain or html etc 
            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":
                data = part["body"].get("data")

                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                    return body 
    else:
        data = payload["body"].get("data")

        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8")
    return body

#file name 
PROCESSED_FILE = "processed_emails.json"

def load_processed_emails():
    try: #try is runing the code but if something happens then the entire code will fail 
        #opens our file in read mode 
        with open(PROCESSED_FILE,"r") as file:
            return set(json.load(file)) # reads json content and turn it into python object 
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_processed_emails(processed_emails):
    with open(PROCESSED_FILE,"w") as file:
        json.dump(list(processed_emails), file,indent=4)
def print_recent_emails():
    service = get_gmail_service()
    
    processed_emails = load_processed_emails()
    result = (
        service.users()
        .messages()
        .list(
            userId="me", #makes sure we are logged in 
            q="is:unread",#checks only unread emails 
            maxResults=10, #sends back max 10 results 
        )
        .execute()
    )

    messages = result.get("messages", [])


    if not messages:
        print("No Email's found")
        return 

    print(f"\nFound {len(messages)} unread emails:")

    for message in messages:
        message_id = message["id"]

        if message_id in processed_emails:
            continue 

        try:
            email = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id = message["id"],
                    format="full",

                )
                .execute()
            )


            headers = email["payload"]["headers"]


            sender = "Unknown"
            subject = "No Subject"

            for header in headers:
                if header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Subject":
                    subject = header["value"]

            
            body = get_email_body(email["payload"])

            score = get_quote_score(subject,body)
            quote_request= is_quote_request(subject,body)
        


            print(f"From {sender}")
            print(f"Subject: {subject}")
            print(f"Quote Score: {score}")

            if quote_request:
                print("QUOTE HAS BEEN DETECTED")
                notification_title= "NEW QUOTE REQUEST"
                
                body_preview = body[:1000]

                notification_message = (
                    f"From: {sender}\n"
                        f"Subject: {subject}\n"
                        f"A Customer has requested a quote"               
                )
                #here we are calling out notification py file 
                notification_sent = send_notification(
                    notification_title,
                    notification_message
                )

                if notification_sent:
                    processed_emails.add(message_id)
                    save_processed_emails(processed_emails)
                #SMS sending code 

            else:
                print("NO QUOTE REQUESTED")

        
                processed_emails.add(message_id)
                save_processed_emails(processed_emails)
        except Exception as error:
            print(f"Error processing email {message_id}: {error}")
if __name__ == "__main__":
    print_recent_emails()



