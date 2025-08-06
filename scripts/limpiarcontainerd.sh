#!/bin/bash

echo "🔍 Listando contenedores detenidos..."
containers=$(sudo ctr -n k8s.io containers list | grep -v RUNNING | awk '{print $1}')
if [ -z "$containers" ]; then
    echo "✅ No hay contenedores detenidos."
else
    echo "🧨 Eliminando contenedores detenidos..."
    for id in $containers; do
        echo "🗑️ Eliminando contenedor: $id"
        sudo ctr -n k8s.io containers delete "$id"
    done
fi

echo ""
echo "🧼 Listando imágenes no referenciadas (no asociadas a contenedores)..."
images=$(sudo ctr -n k8s.io image list | awk '{print $1}' | grep -v NAME)

for img in $images; do
    echo "🧪 Verificando imagen: $img"
    used=$(sudo ctr -n k8s.io containers list | grep "$img")
    if [ -z "$used" ]; then
        echo "🗑️ Eliminando imagen no usada: $img"
        sudo ctr -n k8s.io image remove "$img"
    fi
done

echo ""
echo "🎉 ¡Limpieza terminada! Ahora ejecutá 'df -h' y mirá cómo respira tu nodo 🚀"
