
# Kubernetes Monitoring Dashboard with Prometheus and Grafana

This repository provides a guide for setting up a Kubernetes monitoring dashboard using Prometheus for metrics collection and Grafana for visualization. It also includes configurations for sending alerts to Slack.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Creating a Dashboard](#creating-a-dashboard)
- [Setting Up Alerting](#setting-up-alerting)
- [Testing Slack Notifications](#testing-slack-notifications)
- [Conclusion](#conclusion)

## Prerequisites

- A running Kubernetes cluster.
- `kubectl` configured to interact with your cluster.
- `Helm` installed.

## Installation

### 1. Install Prometheus and Grafana

- Add the necessary Helm repositories:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
- Install Prometheus and Grafana: helm install prometheus prometheus-community/kube-prometheus-stack

### 2. Access Grafana 
- Get the Grafana pod name:
  ```
   kubectl get pods -n default -l app.kubernetes.io/name=grafana
  ```
- Port forward to access Grafana:
  ```
  kubectl port-forward svc/prometheus-grafana 3000:80
  ```
- Open Grafana in a browser:
  ```
  http://localhost:3000
  Username: ****
  Password: *****
  ```

### 3. Creating a Dashboard
- Log in to Grafana.
- Click on the "+" icon in the left sidebar, then select "Dashboard".
- Add a new panel:
- Use Prometheus as the data source.
#### Example queries:

#### CPU Usage:
```
<sum(rate(container_cpu_usage_seconds_total{namespace!=""}[5m])) by (namespace)>
```

#### Memory Usage:
```
<sum(container_memory_usage_bytes{namespace!=""}) by (namespace)>
```
- Configure the visualization type (e.g., graph, gauge) and save the dashboard.

### 4. Setting Up Alerting

1. Configure Alertmanager for Slack Notifications
- Edit the Alertmanager configuration to send alerts to Slack:
```
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
  receiver: 'slack'

receivers:
- name: 'slack'
  slack_configs:
  - api_url: '<YOUR_SLACK_WEBHOOK_URL>'
    channel: '#alerts'
    send_resolved: true
# Replace <YOUR_SLACK_WEBHOOK_URL> with your actual Slack webhook URL.
```
2. Apply the Config
- Edit the Alertmanager ConfigMap: kubectl edit configmap alertmanager-prometheus-kube-prometheus-alertmanager -n default

3. Create Alerts in Prometheus
- Define alerts in Prometheus for high resource usage. Example alert for high CPU usage:
```
groups:
- name: resource-alerts
  rules:
  - alert: HighCpuUsage
    expr: sum(rate(container_cpu_usage_seconds_total{namespace!=""}[5m])) by (namespace) > 0.8
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High CPU usage detected"
      description: "CPU usage is above 80% for more than 5 minutes."
```

### 5. Testing Slack Notifications
You can test Slack notifications by triggering an alert or adjusting resource usage to meet the defined thresholds.

### 6. Conclusion
You now have a functional Grafana dashboard to monitor Kubernetes resource usage and alerting configured to send notifications to Slack. Feel free to customize the dashboard and alert configurations as needed!
For any further questions or assistance, please open an issue in this repository.




