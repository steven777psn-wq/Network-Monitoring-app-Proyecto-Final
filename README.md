# 🛰️ Network Monitoring Project

This project provides a lightweight, containerized network monitoring solution using Python, Prometheus, Alertmanager, and Grafana dashboards. It is designed for educational and practical use, with a focus on clarity, reproducibility, and modular deployment.

---

## 📦 Project Structure

├── src/                        # Source code
│   ├── app/                   # Ping monitoring logic (main.py, ping_utils.py, config.py)
│   └── telegram-webhook/      # Telegram alert relay service (app.py, Dockerfile)

├── infra/                     # Monitoring infrastructure
│   ├── prometheus/           # Prometheus config and alert rules
│   └── alertmanager/         # Alertmanager routing and webhook setup

├── k8s/                       # Kubernetes manifests
│   ├── deployments/          # App and monitor deployments
│   ├── services/             # Service definitions
│   ├── permisos-rbac/        # RBAC roles and bindings
│   └── telegram-webhook/     # Telegram webhook deployment and service

├── dashboards/                # Grafana dashboards (JSON)
├── docker/                    # Docker build context and app packaging
├── scripts/                   # Utility scripts (setup, cleanup)
├── .env                       # Environment variables (excluded from Git)
├── docker-compose.yaml        # Local dev orchestration
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies


---

## 🚀 Features

- ICMP-based latency monitoring using `ping3`
- Prometheus metrics endpoint (`/metrics`)
- Status endpoint (`/status`) for basic health checks
- Custom metric: `device_ping_latency_ms`
- Alertmanager integration with sample alert rules
- Telegram webhook integration for real-time notifications
- Alert routing based on Prometheus job labels
- Docker Compose and Kubernetes support
- Helm-based Prometheus stack deployment
- Grafana integration

---

## 🧪 Metrics Overview

The Python app pings a list of devices and exposes latency metrics:

```Example text:
device_ping_latency_ms{device="123.1.1.1"} 23.5
device_ping_latency_ms{device="123.1.1.1"} -1

• 	-1 indicates unreachable or failed ping.
•       0 also considered unreachable in alert logic
• 	Metrics are refreshed every 30 seconds.

🔧 Local Deployment (Docker Compose)

cd infra/
docker-compose up --build

☁️ Kubernetes Deploymen
1. Apply manifests

kubectl apply -f k8s/YAMLs

Includes:
• 	Deployment and Service for the Python app
• 	Prometheus  for scraping metrics
• 	Alertmanager configuration
•       Telegram webhook deployment and service


2. Deploy Prometheus stack via Helm

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -f infra/prometheus/custom-values.yaml -n monitoring

Note: Ensure your app's Service has correct labels for Prometheus discovery.

3. Access Grafana

kubectl port-forward svc/kube-prometheus-stack-grafana 3001:80 -n monitoring
kubectl get secret kube-prometheus-stack-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d

📈 Planned Grafana Dashboard
•       Latency over time per device
•       Alert visualization for unreachable hosts
•       Outage heatmap per zone


🚨 Alerting System

•       Prometheus alert rules defined in infra/prometheus/prometheus-rule.yaml
•       Alerts include:
        - High latency detection
        - Outage detection (<= 0 latency)
•       Alertmanager routes only alerts from job="network-monitor-service" to Telegram
•       Telegram webhook receives alerts via HTTP and forwards them to your bot


📬 Telegram Webhook Integration
• 	Custom Flask app deployed as a Kubernetes service
• 	Receives alerts from Alertmanager via webhook
• 	Filters and formats messages for Telegram delivery
• 	Alertmanager config uses matchers to route only relevant alerts
        - matchers:
          - job = "network-monitor-service"

🧪 EVE-NG Lab Integration

 This project is also deployed and tested within a custom EVE-NG lab environment, allowing for realistic network simulations scenarios.
• 	The lab includes virtual routers, switches, Win Server, Palo Alto Firewall and Linux & Windows hosts configured to respond to ICMP probes.
• 	Prometheus and the Python monitoring app are deployed in isolated containers within the lab.
• 	This setup enables controlled testing of latency, packet loss, and alerting behavior under various network conditions.
• 	EVE-NG provides a visual topology and supports reproducible demos for RootZone tutorials.

🔍 Monitoring Integration
• 	The Python monitoring app pings key devices across VLANs
• 	Prometheus scrapes metrics from the app, enabling visibility into latency and reachability across zones
• 	Alertmanager triggers notifications when devices become unreachable or latency exceeds thresholds
• 	Telegram webhook delivers alerts in real time to your configured bot/channe







End...


