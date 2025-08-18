# 📡 Network Monitoring with Prometheus and Flask

This project deploys a lightweight network monitoring solution using Python, Flask, and Prometheus. It performs ICMP pings to multiple devices and exposes latency metrics for Prometheus to scrape.

---

## 🚀 Features

- Flask app with /metrics endpoint
- ICMP latency collection via ping3
- Prometheus integration using ServiceMonitor
- Dockerized with Gunicorn for production
- Kubernetes manifests for deployment and monitoring
- Configurable target IPs via environment variables

---


## 📘 Prometheus Monitoring in Kubernetes
Includes a custom Helm configuration to deploy Prometheus in a Kubernetes cluster—ideal for labs and testing.

## 🔧 Installed Components
- Prometheus Server
- Alertmanager
- Node Exporter
- PushGateway
- Kube-State-Metrics

## 🎯 Goals
- Collect node and app metrics
- Visualize metrics via Prometheus UI
- Prepare for Grafana integration
- Optimize for resource-constrained environments
⚙️ Instalacion:
cd /infra/prometheus
helm install prometheus prometheus-community/prometheus -n monitoring -f custom-values.yaml
Note: Persistence is disabled for simplicity on nodes without a StorageClass.


## 📁 Repository Structure

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

## 🛠 Launching the System

helm install prometheus prometheus-community/prometheus -n monitoring -f custom-values.yaml

## 💡 Notes
- IPs are read from TARGET_IPS (comma-separated)
- Defaults to test IPs if undefined
- Failed pings return latency -1


📘 Prometheus Integration Summary

🗓️ Fecha: 6 de agosto, 2025  
🧑‍💻 Autor: Steven

✅ Objetive
Integrate network-monitor with Prometheus to collect ICMP latency metrics.

📦 Components
- Kubernetes
- Prometheus Operator (kube-prometheus-stack)
- ServiceMonitor
- Grafana (optional)
- Flask + prometheus_client

🔧 Pasos realizados

- Verify Metrics Endpoint
curl http://network-monitor-service.monitoring.svc.cluster.local:8080/metrics
- Fix ServiceMonitor Labels
kubectl edit servicemonitor network-monitor-servicemonitor -n monitoring
Update:
metadata:
labels:
release: kube-prometheus-stack
- Verify in Prometheus UI
Check Status → Targets for network-monitor-servicemonitor status.


GRAFANA ACCESS GUIDE - kube-prometheus-stack
============================================

This document explains how to access Grafana deployed via the kube-prometheus-stack Helm chart,
including port-forwarding, credential retrieval, and troubleshooting common errors.

------------------------------------------------------------
1. PORT-FORWARDING TO ACCESS GRAFANA
------------------------------------------------------------

Grafana runs internally on port 3001, but the Kubernetes Service exposes port 80.

To forward it to your local machine:

    kubectl port-forward svc/kube-prometheus-stack-grafana 3001:80 -n monitoring


------------------------------------------------------------
2. RETRIEVE GRAFANA CREDENTIALS
------------------------------------------------------------

Grafana credentials are stored in a Kubernetes Secret.

To retrieve them:

    # Username
    kubectl get secret kube-prometheus-stack-grafana -n monitoring \
      -o jsonpath="{.data.admin-user}" | base64 --decode

    # Password
    kubectl get secret kube-prometheus-stack-grafana -n monitoring \
      -o jsonpath="{.data.admin-password}" | base64 --decode



     

