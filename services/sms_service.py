import os
from twilio.rest import Client
from flask import current_app
from services.llm_service import llm_service

class SmsService:
    def __init__(self):
        pass

    def send_prediction_alert(self, phone_number, predictions, child_name=None):
        if not phone_number:
            print("No phone number provided for SMS.", flush=True)
            return

        phone_str = str(phone_number).strip()
        if not phone_str.startswith('+91'):
            phone_str = '+91' + phone_str
        elif not phone_str.startswith('+'):
            phone_str = '+' + phone_str
        

        account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
        auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
        from_phone = current_app.config.get('TWILIO_PHONE_NUMBER')

        # Extract risk lists
        high_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'HIGH']
        medium_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'MEDIUM']

        # Try to generate personalized message using LLM
        message_body = llm_service.generate_personalized_message(child_name, predictions)
        
        if message_body:
            # Append explicit risk list to guarantee vaccine names are always included
            if high_risk or medium_risk:
                risk_suffix = "\n"
                if high_risk:
                    risk_suffix += f"HIGH Risk: {', '.join(high_risk)}\n"
                if medium_risk:
                    risk_suffix += f"MEDIUM Risk: {', '.join(medium_risk)}"
                message_body = message_body.strip() + risk_suffix
        else:
            # Fallback to default text layout
            if not high_risk and not medium_risk:
                message_body = "VaxRegistry: Your child's vaccination profile is up to date based on our analysis."
            else:
                message_body = "VaxRegistry Alert: Miss risk detected for your child.\n"
                if high_risk:
                    message_body += f"HIGH Risk: {', '.join(high_risk)}\n"
                if medium_risk:
                    message_body += f"MEDIUM Risk: {', '.join(medium_risk)}\n"
                message_body += "Please consult your healthcare provider or visit the nearest vaccination center."

        if not account_sid or not auth_token or not from_phone:
            print("Twilio credentials not configured. Skipping SMS.", flush=True)
            # Log the message body that would have been sent
            print(f"Mock SMS to {phone_str}:\n{message_body}\n", flush=True)
            return False

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=from_phone,
                to=phone_str
            )
            print(f"SMS sent successfully. SID: {message.sid}", flush=True)
            return True
            
        except Exception as e:
            print(f"Failed to send SMS: {e}", flush=True)
            # Also output the message body for debugging in case of sending failures
            print(f"Undelivered SMS Message Body:\n{message_body}\n", flush=True)
            return False

sms_service = SmsService()
