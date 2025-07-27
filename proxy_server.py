from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("EVE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://login.eveonline.com/v2/oauth/token"

app = Flask(__name__)

@app.route('/exchange', methods=['POST'])
def exchange():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    r = requests.post(TOKEN_URL, data=payload, auth=auth)
    if not r.ok:
        return jsonify({"error": "Token exchange failed", "details": r.text}), 400
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
