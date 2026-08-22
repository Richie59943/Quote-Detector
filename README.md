# Quote Email Monitor

An automated Python application that monitors a Gmail inbox for customer requests for quotations (RFQs). When a potential quote request is detected, the application sends an instant push notification through Pushover.

The goal is to make sure new quote requests are noticed quickly without requiring someone to constantly monitor the inbox.

## Features

- Connects securely to Gmail using the Gmail API and OAuth
- Checks for unread emails
- Reads email subjects and message bodies
- Detects potential quote/RFQ requests using keyword scoring
- Prevents duplicate notifications using Gmail message IDs
- Sends push notifications through Pushover
- Handles errors without stopping the monitoring process
- Can run continuously on an always-on Windows computer

## How It Works

```text
Customer Email
      |
      v
    Gmail
      |
      v
 Python Gmail Monitor
      |
      v
 Quote Detector
      |
      v
 Quote Request?
   /       \
 No         Yes
 |           |
Ignore    Pushover
             |
             v
        Phone Notification
