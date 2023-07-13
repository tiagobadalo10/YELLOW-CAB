import os
import subprocess
import threading
import time
import requests
import grpc
import zone_pb2
import zone_pb2_grpc

IP = "127.0.0.1"


def run_thread(app, app_name, port, table_name):
    def run_subprocess():

        os.environ['TABLE_NAME'] = table_name

        result = subprocess.run(['python', app], check=False)

        if result.returncode != 0:
            print(
                f'{app_name}: The subprocess returned a non-zero exit status:', result.returncode)

    thread = threading.Thread(target=run_subprocess)
    thread.daemon = True
    thread.start()

    if app_name == "zones":
        grpc_wait_for_health_check(port)
    else:
        wait_for_health_check(app_name, port)

    return thread


def wait_for_health_check(app_name, port):
    while True:
        try:
            response = requests.get(
                f"http://{IP}:{port}/api/{app_name}/health", timeout=10)
            if response.text == '200\n':
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)


def grpc_wait_for_health_check(port):
    while True:
        try:
            with grpc.insecure_channel(f"{IP}:{port}") as channel:
                stub = zone_pb2_grpc.ZoneServiceStub(channel)
                response = stub.HealthCheck(zone_pb2.HealthCheckRequest())
            if response.status == '200':
                break
        except grpc.RpcError:
            pass
        time.sleep(1)


def init():

    # Obter o diretório atual
    current_dir = os.path.abspath(os.getcwd())

    # Obter o diretório pai do diretório atual
    app_dir = os.path.dirname(current_dir)

    # Obter o diretório pai do diretório app
    yellow_cab_dir = os.path.dirname(app_dir)

    # Obter apps
    biApp = os.path.join(app_dir, "business-intelligence", "main.py")
    statsApp = os.path.join(app_dir, "statistics", "main.py")
    zonesApp = os.path.join(app_dir, "zones", "main.py")

    # Set env vars
    with open(os.path.join(yellow_cab_dir, 'authorization.txt'), encoding="utf-8") as f:
        content = f.read()
    os.environ['POD_NAME'] = "test"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = content
    os.environ['PROJECT_ID'] = "fcul-388721"
    os.environ['DATASET_NAME'] = "zone_locations"
    os.environ['ZONES_CONNECTION'] = "127.0.0.1:50051"

    # Run apps in threads
    run_thread(biApp, "bi", 8082, "stats_table")
    run_thread(statsApp, "stats", 8083, "stats_table")
    run_thread(zonesApp, "zones", 50051, "locations")

    print("Apps are running")

    # Uncomment for debugging purposes
    #while True:
    #    pass


if __name__ == '__main__':
    init()
