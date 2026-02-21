from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_info():
    number = request.args.get('num')
    
    if not number:
        return jsonify({"error": "Number parameter missing. Use ?num=+91xxxx"}), 400

    try:
        # Number parsing
        parsed_number = phonenumbers.parse(number)
        
        if not phonenumbers.is_valid_number(parsed_number):
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400

        # Info gathering
        data = {
            "status": "success",
            "country": geocoder.description_for_number(parsed_number, "en"),
            "operator": carrier.name_for_number(parsed_number, "en"),
            "timezone": list(timezone.time_zones_for_number(parsed_number)),
            "international": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        }
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home route for testing
@app.route('/')
def home():
    return "API is active! Use /api?num=+91xxxxxxxxxx"

# Vercel requirements ke liye
app = app
