from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import requests
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")  # The endpoint name of the flow

# You can tweak the flow by adding a tweaks dictionary
TWEAKS = {
    "Agent-6ghf2": {},
    "ChatInput-atyby": {},
    "ChatOutput-aXeAI": {},
    "Prompt-ZOcYT": {},
    "AstraDBToolComponent-NjvxE": {}
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@app.route('/run_flow', methods=['POST'])
def flow_response():
    """
    Flask route that accepts a POST request with a message and optional tweaks.
    Returns the response from the flow as JSON.
    """
    data = request.get_json()

    # Extract input data
    message = data.get('message', '')
    endpoint = data.get('endpoint', ENDPOINT)
    tweaks = data.get('tweaks', TWEAKS)
    application_token = data.get('application_token', APPLICATION_TOKEN)
    output_type = data.get('output_type', 'chat')
    input_type = data.get('input_type', 'chat')

    # Run the flow
    try:
        response = run_flow(
            message=message,
            endpoint=endpoint,
            output_type=output_type,
            input_type=input_type,
            tweaks=tweaks,
            application_token=application_token
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
