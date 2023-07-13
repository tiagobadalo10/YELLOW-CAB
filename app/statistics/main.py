from threading import Thread
from time import sleep
from config import pod_name
import config
import psutil
from prometheus_client import start_http_server, Gauge

app = config.connex_app
app.add_api(config.basedir / "openapi_statistics.yaml")

# METRICS
MEMORY_USAGE = Gauge('memory_usage_statistics', 'Memory Usage', labelnames=['pod'])
CPU_USAGE = Gauge('cpu_usage_statistics', 'CPU Usage', labelnames=['pod'])


def resources_usage():
    while True:
        MEMORY_USED = psutil.virtual_memory().percent

        MEMORY_USAGE.labels(pod_name).set(MEMORY_USED)

        CPU_USED = psutil.cpu_percent()

        CPU_USAGE.labels(pod_name).set(CPU_USED)
        sleep(5)


Thread(target=resources_usage, daemon=True).start()

if __name__ == "__main__":
    start_http_server(8003)
    app.run(8083)
