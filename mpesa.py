import requests
import base64
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
CONSUMER_KEY = os.getenv("DARAJA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("DARAJA_CONSUMER_SECRET")
BUSINESS_SHORTCODE = os.getenv("DARAJA_SHORTCODE")
PASSKEY = os.getenv("DARAJA_PASSKEY")
CALLBACK_URL = os.getenv("DARAJA_CALLBACK_URL")
PARTY_B = BUSINESS_SHORTCODE  # typically the same as shortcode

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = response.json().get("access_token")
    return access_token

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = BUSINESS_SHORTCODE + PASSKEY + timestamp
    encoded = base64.b64encode(data_to_encode.encode())
    return encoded.decode('utf-8'), timestamp

def process_payment(phone_number, amount):
    """
    Initiates an STK Push request to Safaricom Daraja API
    """
    token = get_access_token()
    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": PARTY_B,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "HomeworkHelper",
        "TransactionDesc": "Payment for AI Homework Assistant"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def check_subscription_status(phone_number):
    """
    Placeholder function – ideally checks a database or API
    """
    # TODO: Link to actual subscription records
    return False
