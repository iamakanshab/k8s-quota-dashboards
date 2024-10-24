
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

## Requesting a K8S Managed Cluster

- Go to https://portal.azure.com/ and create a resource under resource group dvue-aig-infra-rg

## Installation

### 1. Install Prometheus and Grafana

- Add the necessary Helm repositories:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
- Install Prometheus and Grafana:
```
  helm install prometheus prometheus-community/kube-prometheus-stack
```
### 2. View Grafana installs
- Get the Grafana pod name:
```
kubectl get pods -n default -l app.kubernetes.io/name=grafana
```
- Port forward to access Grafana:
```
kubectl port-forward svc/prometheus-grafana 3000:80

### 3. Deploy Grafana the Dashboard WEB UI
```
kubectl create namespace monitoring
helm search repo grafana/grafana
helm install my-grafana grafana/grafana --namespace monitoring
helm list -n monitoring
kubectl get all -n monitoring
```
### 4. Access Grafana
helm get notes my-grafana -n monitoring
kubectl get secret --namespace monitoring my-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 3000
http://localhost:3000
Username: ****
Password: *****
```

### 5. Creating a Dashboard
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

### 6. Setting Up Alerting

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

### 7. Testing Slack Notifications
You can test Slack notifications by triggering an alert or adjusting resource usage to meet the defined thresholds.

### 8. Conclusion
You now have a functional Grafana dashboard to monitor Kubernetes resource usage and alerting configured to send notifications to Slack. Feel free to customize the dashboard and alert configurations as needed!
For any further questions or assistance, please open an issue in this repository.




