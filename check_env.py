import os
import sys
import subprocess

def check_venv():
    # Verifica si estás en un entorno virtual
    venv_path = os.getenv("VIRTUAL_ENV")
    if venv_path:
        print(f"✅ Entorno virtual activo: {venv_path}")
    else:
        print("❌ No estás en un entorno virtual. Activá tu .venv con 'source .venv/bin/activate'")
        return False
    return True

def check_python_path():
    print(f"🔍 Python ejecutándose desde: {sys.executable}")
    if ".venv" in sys.executable:
        print("✅ Intérprete apunta al entorno virtual")
    else:
        print("⚠️ El intérprete no está dentro de .venv")

def check_packages():
    required = ["flask", "prometheus_client", "ping3"]
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ Paquete '{pkg}' instalado")
        except ImportError:
            print(f"❌ Paquete '{pkg}' no encontrado. Instalalo con 'pip install {pkg}'")

if __name__ == "__main__":
    if check_venv():
        check_python_path()
        check_packages()
