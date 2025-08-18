# 🛰️ Network Monitoring Project

This project provides a lightweight, containerized network monitoring solution using Python, Prometheus, Alertmanager, and optional Grafana dashboards. It is designed for educational and practical use, with a focus on clarity, reproducibility, and modular deployment.

---

## 📦 Project Structure

ping-monitor/
├── check_env.py
├── dashboards
│   └── ping-latency-dashboard.json
├── docker
│   └── app
├── docker-compose.yaml
├── Dockerfile
├── .dockerignore
├── docs
│   ├── estructura_actual.txt
│   ├── estructura_actual-v2.txt
│   ├── estructura_actual-v3.txt
│   ├── estructura_actual-v4.txt
│   └── estructura_actual-v5.txt
│   └── estructura_actual-v6.txt
├── .git
│   ├── branches
│   ├── COMMIT_EDITMSG
│   ├── config
│   ├── description
│   ├── filter-repo
│   │   ├── already_ran
│   │   ├── changed-refs
│   │   ├── commit-map
│   │   ├── first-changed-commits
│   │   ├── ref-map
│   │   └── suboptimal-issues
│   ├── HEAD
│   ├── hooks
│   │   ├── applypatch-msg.sample
│   │   ├── commit-msg.sample
│   │   ├── fsmonitor-watchman.sample
│   │   ├── post-update.sample
│   │   ├── pre-applypatch.sample
│   │   ├── pre-commit.sample
│   │   ├── pre-merge-commit.sample
│   │   ├── prepare-commit-msg.sample
│   │   ├── pre-push.sample
│   │   ├── pre-rebase.sample
│   │   ├── pre-receive.sample
│   │   ├── push-to-checkout.sample
│   │   └── update.sample
│   ├── index
│   ├── info
│   │   ├── exclude
│   │   └── refs
│   ├── logs
│   │   ├── HEAD
│   │   └── refs
│   ├── objects
│   │   ├── info
│   │   └── pack
│   ├── ORIG_HEAD
│   ├── packed-refs
│   └── refs
│       ├── heads
│       ├── remotes
│       └── tags
├── .gitignore
├── infra
│   ├── alertmanager
│   │   ├── alertmanager-config.yaml
│   │   └── alertmanager.yaml
│   └── prometheus
│       ├── custom-values.yaml
│       ├── prometheus-rule.yaml
│       └── prometheus.yaml
├── k8s
│   ├── deployments
│   │   ├── flask-app-deployment.yaml
│   │   ├── network-monitor-deployment.yaml
│   │   ├── network-monitor-servicemonitor.yaml
│   │   └── network-monitor-service.yaml
│   ├── monitoring
│   │   ├── monitoring-services.yaml
│   │   └── service-monitors
│   ├── permisos-rbac
│   │   ├── prometheus-rolebinding.yaml
│   │   └── prometheus-role.yaml
│   └── services
│       └── flask-app-service.yaml
├── README.md
├── requirements.txt
├── scripts
│   ├── limpiarcontainerd.sh
│   └── setup_master.sh
├── src
│   └── app
│       ├── config.py
│       ├── .idea
│       ├── main.py
│       ├── ping_utils.py
│       └── __pycache__
├── .venv
│   ├── bin
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── flask
│   │   ├── gunicorn
│   │   ├── ping3
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.10
│   │   ├── python -> python3
│   │   ├── python3 -> /usr/bin/python3
│   │   └── python3.10 -> python3
│   ├── include
│   ├── lib
│   │   └── python3.10
│   ├── lib64 -> lib
│   └── pyvenv.cfg
└── venv
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── Activate.ps1
    │   ├── flask
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.11
    │   ├── python -> python3.11
    │   ├── python3 -> python3.11
    │   └── python3.11 -> /usr/bin/python3.11
    ├── include
    │   └── python3.11
    ├── lib
    │   └── python3.11
    ├── lib64 -> lib
    └── pyvenv.cfg

45 directories, 87 files


---

## 🚀 Features

- ICMP-based latency monitoring using `ping3`
- Prometheus metrics endpoint (`/metrics`)
- Status endpoint (`/status`) for basic health checks
- Custom metric: `device_ping_latency_ms`
- Alertmanager integration with sample alert rules
- Docker Compose and Kubernetes support
- Helm-based Prometheus stack deployment
- Grafana integration (planned)

---

## 🧪 Metrics Overview

The Python app pings a list of devices and exposes latency metrics:

```text
device_ping_latency_ms{device="8.8.8.8"} 23.5
device_ping_latency_ms{device="1.1.1.1"} -1

• 	-1 indicates unreachable or failed ping.
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

2. Deploy Prometheus stack via Helm

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack

Note: Ensure your app's Service has correct labels for Prometheus discovery.

3. Access Grafana

kubectl port-forward svc/monitoring-grafana 3001:80
kubectl get secret monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d

📈 Planned Grafana Dashboard
• 	Latency over time per device
• 	Alert visualization for unreachable hosts

🚨 Alertin

/Prometheus/ prometheus-rule.yaml


🧪 EVE-NG Lab Integration

This project is also deployed and tested within a custom EVE-NG lab environment, allowing for realistic network simulations scenarios.
• 	The lab includes virtual routers, switches, Win Server, Palo Alto Firewall and Linux & Windows hosts configured to respond to ICMP probes.
• 	Prometheus and the Python monitoring app are deployed in isolated containers within the lab.
• 	This setup enables controlled testing of latency, packet loss, and alerting behavior under various network conditions.
• 	EVE-NG provides a visual topology and supports reproducible demos for RootZone tutorials.

🔍 Monitoring Integration
• 	The Python monitoring app is deployed inside the lab and pings key devices across VLANs.
• 	Prometheus scrapes metrics from the app, enabling visibility into latency and reachability across zones.
• 	Alertmanager triggers notifications when devices become unreachable or latency exceeds thresholds.


