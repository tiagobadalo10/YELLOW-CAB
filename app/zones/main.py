from threading import Thread
from time import sleep
from concurrent import futures
import grpc
import psutil
import zone_pb2_grpc
from prometheus_client import start_http_server, Gauge
from zones import ZoneService
from config import pod_name

MEMORY_USAGE = Gauge('memory_usage_zones', 'Memory Usage in Bytes', labelnames=['pod'])
CPU_USAGE = Gauge('cpu_usage_zones', 'CPU Usage in Percent', labelnames=['pod'])


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zone_pb2_grpc.add_ZoneServiceServicer_to_server(ZoneService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


def resources_usage():
    while True:
        MEMORY_USED = psutil.virtual_memory().percent

        MEMORY_USAGE.labels(pod_name).set(MEMORY_USED)

        CPU_USED = psutil.cpu_percent()

        CPU_USAGE.labels(pod_name).set(CPU_USED)
        sleep(5)


Thread(target=resources_usage, daemon=True).start()

if __name__ == "__main__":
    start_http_server(8051)
    serve()
