#main is going to continuously run our other programs so we dont have to keep running our gmail.py file manually

import time 

from gmail_client import print_recent_emails

CHECK_INTERVAL = 3600 #time check is every hour 

def main():
    print("Quote Email Monitor Started.")
    print(f"Checking Gmail every hour")

    while True: # a while loop going on forever 
        try:
            print("Checking for new emails..")

            print_recent_emails()

        except Exception as error:
            print(f"Monitor error: {error}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
