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



