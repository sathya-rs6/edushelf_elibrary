from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("edushelf-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    return jsonify({"message": "EduShelf API is running!"})

@app.route('/login', methods=['POST'])
def login():
    try:
        id_token = request.json.get('idToken')
        decoded = auth.verify_id_token(id_token)
        return jsonify({"success": True, "uid": decoded['uid'], "email": decoded['email']})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401

@app.route('/signup', methods=['POST'])
def signup():
    try:
        id_token = request.json.get('idToken')
        # Optionally parse user info:
        name = request.json.get('name')
        email = request.json.get('email')
        # password = request.json.get('password')  # usually handled by Firebase client side
        # Verify the ID token
        decoded = auth.verify_id_token(id_token)
        # Optionally add further user data processing here (e.g. database save)
        return jsonify({"success": True, "uid": decoded['uid'], "email": decoded['email']})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
