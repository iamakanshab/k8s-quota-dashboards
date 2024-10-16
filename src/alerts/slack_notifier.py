import os
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message):
    """Send alert message to Slack channel."""
    if not SLACK_WEBHOOK_URL:
        raise ValueError("Slack webhook URL not configured")

    payload = {
        "text": message
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned error {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_slack_alert("Test alert: Kubernetes quota exceeded!")
