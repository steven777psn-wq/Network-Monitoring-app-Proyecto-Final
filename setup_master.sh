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
