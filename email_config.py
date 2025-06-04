import json
import smtplib
import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build

def email_body(): 
    with open("matched_jobs.json", "r") as file:
        jobs = json.load(file)

    email_body = "Here are the latest job matches:\n\n"

    for job in jobs:
        title = job["title"]
        company = job["company"]
        filters = job["matched_filters"]
        salary = job["salary"] if job["salary"] != 0 else "Not specified"
        location = job["location"]
        url = job["url"]  # Placeholder—update with actual link
        filters_text = ', '.join([f"{key}: {value}" for key, value in filters.items()])

        email_body += f"📌 {title}\n 🏢 {company}\n   🌍 Location: {location}\n   💰 Salary: {salary}\n  It matched the following specifications: {filters_text}\n   🔗 [Apply Here]: ({url})\n\n"

    return email_body  # ✅ Check formatting before sending

# Set up the email
def get_credentials():
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def send_email():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEMultipart()
    message["to"] = "tarantulaspider00@gmail.com"
    message["subject"] = "🔥 New Job Matches!"

    body = email_body()
    message.attach(MIMEText(body, "plain"))

    raw_message = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    send_message = {"raw": raw_message}

    service.users().messages().send(userId="me", body=send_message).execute()
    print("✅ Email sent successfully!")
