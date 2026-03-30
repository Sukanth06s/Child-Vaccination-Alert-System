import os
from twilio.rest import Client
from flask import current_app

class SmsService:
    def __init__(self):
        pass

    def send_prediction_alert(self, phone_number, predictions):
        if not phone_number:
            print("No phone number provided for SMS.")
            return

        phone_str = str(phone_number).strip()
        if not phone_str.startswith('+'):
            phone_str = '+' + phone_str

        account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
        auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
        from_phone = current_app.config.get('TWILIO_PHONE_NUMBER')

        if not account_sid or not auth_token or not from_phone:
            print("Twilio credentials not configured. Skipping SMS.")
            # Mocking SMS log for debugging without credentials
            high_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'HIGH']
            medium_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'MEDIUM']
            msg = "VaxRegistry Mock SMS: "
            if high_risk or medium_risk:
                msg += f"Risk detected. High: {high_risk}, Medium: {medium_risk}"
            else:
                msg += "All good."
            print(f"To {phone_str}: {msg}")
            return

        try:
            client = Client(account_sid, auth_token)
            
            # Format message
            high_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'HIGH']
            medium_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'MEDIUM']

            if not high_risk and not medium_risk:
                message_body = "VaxRegistry: Your child's vaccination profile is up to date based on our analysis."
            else:
                message_body = "VaxRegistry Alert: Miss risk detected for your child.\n"
                if high_risk:
                    message_body += f"HIGH Risk: {', '.join(high_risk)}\n"
                if medium_risk:
                    message_body += f"MEDIUM Risk: {', '.join(medium_risk)}\n"
                message_body += "Please consult your healthcare provider or visit the nearest vaccination center."

            message = client.messages.create(
                body=message_body,
                from_=from_phone,
                to=phone_str
            )
            print(f"SMS sent successfully. SID: {message.sid}")
            
        except Exception as e:
            print(f"Failed to send SMS: {e}")

sms_service = SmsService()
