from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from ping3 import ping
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Ruta de log segura y accesible
LOG_PATH = '/home/evargas/ping-monitor/docs/logs/ping_monitor.log'

# Reforzar el logger para que Gunicorn no lo ignore
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Evitar duplicación de handlers
if not any(isinstance(h, logging.FileHandler) and h.baseFilename == LOG_PATH for h in logger.handlers):
    handler = logging.FileHandler(LOG_PATH)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Métrica para latencia
latency = Gauge('device_ping_latency_ms', 'Latencia ICMP en ms a dispositivos', ['ip'])

# Obtener lista de IPs desde variable de entorno
target_ips = os.getenv('TARGET_IPS', '10.1.1.30,123.1.1.11,172.16.1.54,123.1.1.1')
targets = [ip.strip() for ip in target_ips.split(',')]

@app.route('/')
def home():
    return 'Network Monitor App - /metrics'

@app.route('/metrics')
def metrics():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, threaded=True)
