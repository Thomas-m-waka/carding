import requests
import json
from django.shortcuts import get_object_or_404
from otii.models import PasswordResetToken
from django.utils import timezone
import os 

def send_sms(phone_number, message):
    url = "https://sms.textsms.co.ke/api/services/sendsms"
    payload = {
        "mobile": f'+254{phone_number}',
        "response_type": "json",
        "partnerID": '10338',
        "shortcode":'TextSMS',
        'apikey': '633b3259c2f504f6f4d81be0a1528626',
        "message": message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text

def verify_verification_code(user, verification_code):

    reset_token = get_object_or_404(PasswordResetToken, user=user)
   
    if reset_token.verification_code == verification_code:
        # Check if the token has expired (e.g., within 5 minutes)
        if timezone.now() - reset_token.created_at <= timezone.timedelta(minutes=5):
            return user
    return None