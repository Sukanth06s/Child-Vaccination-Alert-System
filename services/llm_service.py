import requests
import json
from flask import current_app

class LlmService:
    def __init__(self):
        pass

    def generate_personalized_message(self, child_name, predictions):
        """
        Generates a personalized, friendly alert message for parents about their child's vaccination.
        If API call fails or key is missing, returns None.
        """
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            print("Gemini API key not configured. Skipping LLM message generation.", flush=True)
            return None

        name = child_name or "your child"

        # Format list of risk levels
        high_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'HIGH']
        medium_risk = [p['vaccine_name'].upper() for p in predictions if p['confidence_level'].upper() == 'MEDIUM']

        if not high_risk and not medium_risk:
            prompt = (
                f"Generate a friendly, reassuring notification message for a parent about their child ({name})'s vaccinations. "
                "The analysis shows their vaccination profile is fully up to date. "
                "Requirements: Keep it concise (under 160 characters), warm, professional, and optimized for an SMS. "
                "Do not use any markdown formatting (like asterisks, hashtags, or markdown bold)."
            )
        else:
            risk_details = []
            if high_risk:
                risk_details.append(f"HIGH risk of missing: {', '.join(high_risk)}")
            if medium_risk:
                risk_details.append(f"MEDIUM risk of missing: {', '.join(medium_risk)}")
            
            risk_str = "\n".join(risk_details)

            prompt = (
                f"Generate a friendly, warm, yet urgent notification alert message for a parent. "
                f"The parent's child is named '{name}'. "
                f"Our analysis indicates the following vaccination status risks:\n"
                f"{risk_str}\n\n"
                "Requirements:\n"
                "1. Remind the parent gently but clearly about these potential missing vaccinations.\n"
                "2. Encourage them to consult their doctor or visit the nearest healthcare center.\n"
                "3. Keep the total message very concise (under 240 characters) so it fits in a single or double SMS segment.\n"
                "4. Do NOT use any markdown styling (no *asterisks*, no # hashtags, no bold texts, no bullet points) as this will be sent via SMS text message.\n"
                "5. Keep the tone empathetic and professional."
            )

        try:
            # Call Gemini API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 1000
                }
            }
            
            print(f"Calling Gemini API for personalization...", flush=True)
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                res_data = response.json()
                # Extract text response
                text_response = res_data['candidates'][0]['content']['parts'][0]['text']
                clean_message = text_response.strip()
                print(f"Successfully generated LLM personalized alert.", flush=True)
                return clean_message
            else:
                print(f"Gemini API returned status code {response.status_code}: {response.text}", flush=True)
                return None
        except Exception as e:
            print(f"Failed to generate LLM message: {e}", flush=True)
            return None

llm_service = LlmService()
