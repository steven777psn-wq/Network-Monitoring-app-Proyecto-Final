#!/bin/bash
set -e

# Variables personalizadas
MASTER_IP="192.168.5.190"
POD_CIDR="10.244.0.0/16"
FLANNEL_YAML="https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml"

echo "[+] Actualizando e instalando dependencias..."
sudo apt update
sudo apt install -y curl apt-transport-https ca-certificates gnupg lsb-release

echo "[+] Asegurando configuración del kernel y swap..."
sudo swapoff -a
sudo modprobe br_netfilter
echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee /etc/sysctl.d/k8s.conf
sudo sysctl --system

echo "[+] Configurando permisos para containerd..."
sudo groupadd -f containerd
sudo chgrp containerd /run/containerd/containerd.sock
sudo usermod -aG containerd "$(whoami)"
newgrp containerd

echo "[+] Reinicializando cluster Kubernetes..."
sudo kubeadm reset -f
sudo kubeadm init --apiserver-advertise-address=$MASTER_IP --pod-network-cidr=$POD_CIDR

echo "[+] Configurando kubectl para el usuario actual..."
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo "[+] Aplicando red Flannel..."
kubectl apply -f $FLANNEL_YAML

echo "[✓] Setup completo. ¡Listo para monitorizar!"




startup 2.0 

#!/bin/bash

echo "🔄 Reiniciando entorno del laboratorio..."

# Reinicio de Docker
echo "🔧 Reiniciando servicio Docker..."
sudo systemctl restart docker

# Reinicio de contenedores esenciales
echo "🐳 Reiniciando contenedores..."
docker container restart ping-monitor
docker container restart prometheus
docker container restart grafana

# Verificación de estado de contenedores
echo "📋 Estado actual de contenedores:"
docker ps --filter name=ping-monitor --filter name=prometheus --filter name=grafana

# Reinicio de Kubernetes (usando kubeadm o microk8s si aplica)
echo "📦 Reiniciando servicios de Kubernetes..."
sudo systemctl restart kubelet
kubectl rollout restart deployment prometheus-deployment -n monitoring
kubectl rollout restart deployment grafana-deployment -n monitoring

# Limpieza de pods fallidos (opcional)
kubectl get pods --all-namespaces | grep CrashLoopBackOff | awk '{print $2, $1}' | xargs -r -n2 kubectl delete pod -n

# Aplicación de manifiestos personalizados si están versionados
echo "📁 Reaplicando manifiestos YAML..."
kubectl apply -f ~/lab/manifests/

# Confirmación final
echo "✅ Entorno reiniciado. Verifica en Grafana y Prometheus que todo esté operativo."











#Recontruir Docker con Docker-compose. Yaml
docker compose build         # Construye ping-monitor
docker compose up -d        # Levanta todo en segundo plano
docker compose ps           # Muestra el estado de los servicios






