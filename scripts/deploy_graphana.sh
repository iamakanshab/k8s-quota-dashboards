#!/bin/bash

# Apply the Grafana Kubernetes manifests
kubectl apply -f config/grafana/grafana-deployment.yaml

# Port forward Grafana for local access (optional)
kubectl port-forward svc/grafana 3000:3000
