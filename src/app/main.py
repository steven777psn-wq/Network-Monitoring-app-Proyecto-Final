from flask import Flask, Response, request
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from ping3 import ping
import os
import logging
import sys

app = Flask(__name__)

# Ruta del archivo de logs
LOG_PATH = "/app/logs/ping_monitor.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Logger robusto y compartido entre procesos
def get_logger():
    logger = logging.getLogger("ping-monitor")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(LOG_PATH, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = get_logger()

# Middleware para registrar cada petición
@app.before_request
def log_request():
    logger = get_logger()
    logger.info(f"Petición recibida: {request.method} {request.path} desde {request.remote_addr}")

# Métrica Prometheus
latency = Gauge('device_ping_latency_ms', 'Latencia ICMP en ms a dispositivos', ['ip'])

# Lista de IPs desde variable de entorno
target_ips = os.getenv('TARGET_IPS', '10.1.1.30,123.1.1.11,172.16.1.54,123.1.1.1')
targets = [ip.strip() for ip in target_ips.split(',')]

@app.route('/')
def home():
    return 'Network Monitor App - /metrics'

@app.route('/metrics')
def metrics():
    logger = get_logger()
    logger.info("Scrape recibido desde Prometheus")
    for ip in targets:
        try:
            result = ping(ip, timeout=2)
            if result is not None:
                latency.labels(ip=ip).set(round(result * 1000, 2))
                logger.info(f"Ping exitoso a {ip}: {round(result * 1000, 2)} ms")
            else:
                latency.labels(ip=ip).set(-1)
                logger.warning(f"No se obtuvo respuesta de {ip}")
        except Exception as e:
            latency.labels(ip=ip).set(-1)
            logger.error(f"Error al hacer ping a {ip}: {e}")

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Solo para usar con Flask directamente (no Gunicorn "check Dockerfile") descomentar las 2 lineas de abajo
# if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8080)
