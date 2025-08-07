# 📡 Monitorización de Red con Prometheus y Flask

Este proyecto tiene como objetivo desplegar una solución ligera de monitoreo de red usando Python, Flask y Prometheus. La aplicación permite realizar pings a múltiples dispositivos definidos por IP y expone métricas de latencia ICMP que pueden ser recolectadas por Prometheus.

---

## 🚀 Características Principales

- 📦 App escrita en Flask, con métricas expuestas vía `/metrics`
- 📈 Recolección de métricas ICMP por IP usando `ping3`
- 🧠 Integración con Prometheus vía `ServiceMonitor` en Kubernetes
- 🐳 Dockerfile optimizado para producción con Gunicorn
- ☸️ Manifiestos de Kubernetes para despliegue, servicio y monitoreo
- 🔧 Configuración modular con variables de entorno para IPs objetivo

---

## 🧬 Estructura del proyecto




## 📘 Monitorización con Prometheus en Kubernetes
Este repositorio contiene la configuración personalizada para desplegar Prometheus utilizando Helm en un clúster Kubernetes, ideal para entornos de laboratorio y pruebas.

## 🔧 Componentes Instalados
- Prometheus Server
- Alertmanager
- Node Exporter
- PushGateway
- Kube-State-Metrics

## 🎯 Objetivos
- Recolectar métricas de los nodos y aplicaciones.
- Visualizar métricas vía Prometheus UI.
- Preparar el entorno para conectar con Grafana.
- Optimizar el despliegue para entornos con recursos limitados.
⚙️ Instalacion:
cd /infra/prometheus #ahi se encuentra el custom value.yaml
helm install prometheus prometheus-community/prometheus \
  -n monitoring \
  -f custom-values.yaml
Nota: La persistencia está desactivada para facilitar la instalación sin volúmenes en nodos sin StorageClass.

## 📁 Estructura del repositorio

ping-monitor/
├── Infra/Prometheus/ custom-values.yaml         # Configuración para Helm
├── manifests/                 # Archivos YAML opcionales
├── README.md                  # Documentación del proyecto
└── .gitignore                 # Archivos excluidos del repo


## 🚨 Advertencia
Este despliegue no persiste datos. Todos los datos se borran si el pod se reinicia. Ideal para pruebas, no recomendado para producción.

Cuando lo tengas en Git, podés agregar etiquetas y documentar tus pruebas, alertas, y dashboards. ¿Querés que después te ayude a crear un panel en Grafana para que se integre directo con este setup? Lo armamos paso a paso 💡📊


---

## 🛠 Cómo levantar el sistema

```bash
# Instalar Prometheus con Helm y configuración personalizada
helm install prometheus prometheus-community/prometheus \
  -n monitoring \
  -f custom-values.yaml


## 💡 Notas
- La app lee las IPs desde la variable de entorno TARGET_IPS, separadas por comas.
- Si no se define la variable, se usan IPs por defecto para prueba.
- Los pings fallidos se marcan con latencia -1.


📘 network-monitor Integration with Prometheus

🗓️ Fecha: 6 de agosto, 2025  
🧑‍💻 Autor: Steven

✅ Objetivo
Integrar el servicio network-monitor con Prometheus para recolectar métricas de latencia ICMP hacia dispositivos de red.

📦 Componentes involucrados
- Kubernetes
- Prometheus Operator (kube-prometheus-stack)
- ServiceMonitor
- Grafana (opcional para visualización)
- Flask + prometheus_client (en el servicio)

🔧 Pasos realizados

1. Verificación del endpoint de métricas

curl http://network-monitor-service.monitoring.svc.cluster.local:8080/metrics

Se confirmó que el endpoint responde correctamente con métricas como:
- device_ping_latency_ms{ip="..."} → Latencia ICMP
- Métricas estándar de Python y del proceso

2. Corrección del ServiceMonitor

Se detectó que Prometheus no estaba scrapeando el servicio debido a un label incorrecto.

Solución aplicada:
- Se editó el recurso activo:
  kubectl edit servicemonitor network-monitor-servicemonitor -n monitoring

- Se actualizó el archivo YAML:
  metadata:
    labels:
      release: kube-prometheus-stack

Esto asegura compatibilidad con el selector de serviceMonitorSelector usado por Prometheus.

3. Verificación en Prometheus

- Se accedió a la UI de Prometheus
- En Status → Targets, se confirmó que el job network-monitor-servicemonitor aparece como UP

📌 Próximos pasos
- [ ] Crear panel en Grafana para visualizar device_ping_latency_ms
- [ ] Configurar alertas para valores -1.0 o latencias elevadas
- [ ] Expandir monitoreo a más dispositivos o protocolos

📝 Notas
Este README documenta la integración exitosa del servicio de monitoreo de red con Prometheus. El sistema ahora puede recolectar métricas de latencia ICMP y está listo para visualización y alertas.



GRAFANA ACCESS GUIDE - kube-prometheus-stack
============================================

This document explains how to access Grafana deployed via the kube-prometheus-stack Helm chart,
including port-forwarding, credential retrieval, and troubleshooting common errors.

------------------------------------------------------------
1. PORT-FORWARDING TO ACCESS GRAFANA
------------------------------------------------------------

Grafana runs internally on port 3000, but the Kubernetes Service exposes port 80.

To forward it to your local machine:

    kubectl port-forward svc/kube-prometheus-stack-grafana 3001:80 -n monitoring

NOTE:
- If port 3001 is already in use, choose another (e.g. 3002, 8080, etc.)

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

In this environment:
- Username: admin
- Password: prom-operator

------------------------------------------------------------
3. COMMON ERRORS & FIXES
------------------------------------------------------------

❌ ERROR: "Service does not have a service port 3000"

FIX:
Use the correct exposed port (80), not Grafana's internal 3000.

    kubectl port-forward svc/kube-prometheus-stack-grafana 3001:80 -n monitoring

❌ ERROR: "address already in use"

FIX:
- Check which process is using the port:

     

