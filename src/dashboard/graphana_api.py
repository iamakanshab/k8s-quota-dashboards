import requests
import os

GRAFANA_API_URL = os.getenv("GRAFANA_API_URL")
GRAFANA_API_TOKEN = os.getenv("GRAFANA_API_TOKEN")

def get_dashboard(dashboard_uid):
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_TOKEN}"
    }
    url = f"{GRAFANA_API_URL}/api/dashboards/uid/{dashboard_uid}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get dashboard: {response.status_code} - {response.text}")

def update_dashboard(dashboard_json):
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{GRAFANA_API_URL}/api/dashboards/db"
    response = requests.post(url, headers=headers, json=dashboard_json)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to update dashboard: {response.status_code} - {response.text}")

if __name__ == "__main__":
    dashboard_uid = "your_dashboard_uid"
    dashboard = get_dashboard(dashboard_uid)
    print(dashboard)
